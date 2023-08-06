import json
import unittest

from mock import MagicMock, patch

from tcell_agent.instrumentation.djangoinst.meta import MAXIMUM_BODY_SIZE, \
     initialize_tcell_context, get_appsensor_meta, set_response, \
     check_body_for_json, parse_body, set_request
from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.tests.support.builders import ContextBuilder


class InitializeTcellContextTest(unittest.TestCase):
    def initialize_tcell_context_test(self):
        request = MagicMock()
        request.META = MagicMock(return_value={"HTTP_REFERER": "referrer",
                                               "HTTP_USER_AGENT": "user-agent"})
        request.method = MagicMock(return_value="GET")
        request.path = MagicMock(return_value="/some/path")
        request.get_full_path = MagicMock(return_value="/some/path?param=hi")
        request.build_absolute_uri = MagicMock(return_value="http://localhost/some/path?param=hi")
        with patch("tcell_agent.instrumentation.djangoinst.meta.better_ip_address",
                   return_value="1.1.1.1") as patched_better_ip_address:
            with patch("tcell_agent.instrumentation.djangoinst.meta.get_route_id",
                       return_value="route-id") as patched_get_route_id:
                initialize_tcell_context(request)
                tcell_context = request._tcell_context
                self.assertTrue(patched_better_ip_address.called)
                self.assertTrue(patched_get_route_id.called)
                self.assertIsNotNone(tcell_context.transaction_id)
                self.assertIsNotNone(tcell_context.referrer, "referrer")
                self.assertIsNotNone(tcell_context.user_agent, "user-agent")
                self.assertIsNotNone(tcell_context.remote_address, "1.1.1.1")
                self.assertIsNotNone(tcell_context.method, "GET")
                self.assertIsNotNone(tcell_context.path, "/some/path")
                self.assertIsNotNone(tcell_context.fullpath, "/some/path?param=hi")
                self.assertIsNotNone(tcell_context.uri, "http://localhost/some/path?param=hi")
                self.assertIsNotNone(tcell_context.route_id, "route-id")


class GetAppsensorMetaTest(unittest.TestCase):
    class FakeRequest(object):
        def __init__(self, tcell_context, encoding):
            self._tcell_context = tcell_context
            self.encoding = encoding

    def get_appsensor_meta_test(self):
        tcell_context = ContextBuilder().update_attribute(
            "remote_address", "1.1.1.1"
        ).update_attribute(
            "method", "GET"
        ).update_attribute(
            "user_agent", "user-agent"
        ).update_attribute(
            "uri", "http://localhost/some/path?param=hi"
        ).update_attribute(
            "path", "/some/path"
        ).update_attribute(
            "route_id", "route-id"
        ).update_attribute(
            "session_id", "session-id"
        ).update_attribute(
            "user_id", "user-id"
        ).build()
        request = self.FakeRequest(tcell_context, "UTF-8")

        appsensor_meta = get_appsensor_meta(request)
        self.assertEqual(appsensor_meta.remote_address, "1.1.1.1")
        self.assertEqual(appsensor_meta.method, "GET")
        self.assertEqual(appsensor_meta.user_agent_str, "user-agent")
        self.assertEqual(appsensor_meta.location, "http://localhost/some/path?param=hi")
        self.assertEqual(appsensor_meta.path, "/some/path")
        self.assertEqual(appsensor_meta.route_id, "route-id")
        self.assertEqual(appsensor_meta.session_id, "session-id")
        self.assertEqual(appsensor_meta.user_id, "user-id")
        self.assertEqual(appsensor_meta.encoding, "UTF-8")


class SetResponseTest(unittest.TestCase):
    class FakeResponse(object):
        def __init__(self, status_code, content):
            self.status_code = status_code
            self.content = content

    def set_response_test(self):
        appsensor_meta = AppSensorMeta()
        appsensor_meta.response_processed = True
        appsensor_meta.response_content_bytes_len = -1
        appsensor_meta.response_code = "500"
        set_response(
            appsensor_meta,
            self.FakeResponse,
            self.FakeResponse("200", "")
        )
        self.assertTrue(appsensor_meta.response_processed)
        self.assertEqual(appsensor_meta.response_content_bytes_len, -1)
        self.assertEqual(appsensor_meta.response_code, "500")

        appsensor_meta.response_processed = False
        set_response(
            appsensor_meta,
            self.FakeResponse,
            self.FakeResponse("200", "some content")
        )
        self.assertTrue(appsensor_meta.response_processed)
        self.assertEqual(appsensor_meta.response_content_bytes_len, 12)
        self.assertEqual(appsensor_meta.response_code, "200")


class CheckBodyForJsonTest(unittest.TestCase):
    def request_body_exceeds_maximum_test(self):
        request_body = "".join(["a" * MAXIMUM_BODY_SIZE])
        post_dict, json_dict = check_body_for_json(
            {"post-param": "value"}, request_body, "UTF-8"
        )
        self.assertEqual(post_dict, {"post-param": "value"})
        self.assertEqual(json_dict, {})

    def request_body_is_a_json_dict_test(self):
        request_body = json.dumps({
            "json-param": "value"
        })
        post_dict, json_dict = check_body_for_json(
            {"post-param": "value"}, request_body, "UTF-8"
        )
        self.assertEqual(post_dict, {})
        self.assertEqual(json_dict, {"json-param": "value"})

    def request_body_is_a_json_list_test(self):
        request_body = json.dumps(["json-item"])
        post_dict, json_dict = check_body_for_json(
            {"post-param": "value"}, request_body, "UTF-8"
        )
        self.assertEqual(post_dict, {})
        self.assertEqual(json_dict, ["json-item"])

    def request_body_is_a_malformed_json_string_test(self):
        request_body = "{malformed-json: value}"
        post_dict, json_dict = check_body_for_json(
            {"post-param": "value"}, request_body, "UTF-8"
        )
        self.assertEqual(post_dict, {"post-param": "value"})
        self.assertEqual(json_dict, {})

    def request_body_is_a_form_post_test(self):
        request_body = "first_name=TCell&last_name=Tester"
        post_dict, json_dict = check_body_for_json(
            {"post-param": "value"}, request_body, "UTF-8"
        )
        self.assertEqual(post_dict, {"post-param": "value"})
        self.assertEqual(json_dict, {})


class ParseBodyTest(unittest.TestCase):
    class FakeRequest(object):
        def __init__(self, content_type, post_dict, body):
            self.META = {
                "CONTENT_TYPE": content_type
            }
            self.POST = post_dict
            self.body = body

    def content_length_is_none_test(self):
        post_body, json_dict = parse_body(
            self.FakeRequest(None, {"post": "value"}, ""), None, "UTF-8"
        )
        self.assertEqual(post_body, {"post": "value"})
        self.assertEqual(json_dict, {})

    def content_length_is_zero_test(self):
        post_body, json_dict = parse_body(
            self.FakeRequest(None, {"post": "value"}, ""), 0, "UTF-8"
        )
        self.assertEqual(post_body, {"post": "value"})
        self.assertEqual(json_dict, {})

    def content_length_exceeds_maximum_test(self):
        post_body, json_dict = parse_body(
            self.FakeRequest(None, {"post": "value"}, ""), MAXIMUM_BODY_SIZE, "UTF-8"
        )
        self.assertEqual(post_body, {"post": "value"})
        self.assertEqual(json_dict, {})

    def content_type_is_multipart_test(self):
        request = self.FakeRequest("Multipart/Form-Data; UTF-8",
                                   {"post": "value"},
                                   "bounday---- alkdsjfladjf ----")
        post_body, json_dict = parse_body(
            request, len(request.body), "UTF-8"
        )
        self.assertEqual(post_body, {"post": "value"})
        self.assertEqual(json_dict, {})

    def parse_body_test(self):
        with patch("tcell_agent.instrumentation.djangoinst.meta.check_body_for_json",
                   return_value=[{}, {}]) as patched_check_body_for_json:
            request = self.FakeRequest("application/Json; UTF-8",
                                       {"post": "value"},
                                       "{\"param\":\"val\"}")
            parse_body(
                request, len(request.body), "UTF-8"
            )
            self.assertTrue(patched_check_body_for_json.called)
            args, kwargs = patched_check_body_for_json.call_args
            self.assertEqual(kwargs, {})
            self.assertEqual(args, ({"post": "value"}, "{\"param\":\"val\"}", "UTF-8",))


class SetRequestTest(unittest.TestCase):
    class FakeFile(object):
        def __init__(self, filename):
            self.name = filename

    class FakeFiles(object):
        def __init__(self, filenames):
            self.filenames = filenames

        def getlist(self, filename):  # pylint: disable=no-self-use
            return [SetRequestTest.FakeFile(filename)]

        def keys(self):
            return self.filenames

    class FakeRequest(object):
        def __init__(self,
                     content_length=None,
                     get_dict=None,
                     cookies_dict=None,
                     filenames=None):
            self.META = {
                "CONTENT_LENGTH": content_length
            }
            self.GET = get_dict
            self.COOKIES = cookies_dict
            self.FILES = SetRequestTest.FakeFiles(filenames)

    def already_processed_request_test(self):
        appsensor_meta = AppSensorMeta()
        appsensor_meta.request_processed = True
        appsensor_meta.get_dict = {}
        appsensor_meta.cookie_dict = {}
        appsensor_meta.headers_dict = {}
        appsensor_meta.json_dict = {}
        appsensor_meta.post_dict = {}
        appsensor_meta.request_content_bytes_len = -1
        appsensor_meta.files_dict = {}

        request = self.FakeRequest()
        set_request(appsensor_meta, request)

        self.assertTrue(appsensor_meta.request_processed)
        self.assertEqual(appsensor_meta.get_dict, {})
        self.assertEqual(appsensor_meta.cookie_dict, {})
        self.assertEqual(appsensor_meta.headers_dict, {})
        self.assertEqual(appsensor_meta.json_dict, {})
        self.assertEqual(appsensor_meta.post_dict, {})
        self.assertEqual(appsensor_meta.request_content_bytes_len, -1)
        self.assertEqual(appsensor_meta.files_dict, {})

    def set_request_test(self):
        appsensor_meta = AppSensorMeta()
        appsensor_meta.encoding = "UTF-8"
        appsensor_meta.request_processed = False
        appsensor_meta.get_dict = {}
        appsensor_meta.cookie_dict = {}
        appsensor_meta.headers_dict = {}
        appsensor_meta.json_dict = {}
        appsensor_meta.request_content_bytes_len = -1
        appsensor_meta.files_dict = {}

        request = self.FakeRequest(content_length=100,
                                   get_dict={"get-param": "value"},
                                   cookies_dict={"cookie-param": "value"},
                                   filenames=["filename-one", "filename-two"])
        with patch("tcell_agent.instrumentation.djangoinst.meta.parse_body",
                   return_value=[{"post-param": "value"},
                                 {"json-param": "value"}]) as patched_parse_body:
            set_request(appsensor_meta, request)
            self.assertTrue(patched_parse_body.called)
            self.assertTrue(appsensor_meta.request_processed)
            self.assertEqual(appsensor_meta.get_dict, {"get-param": "value"})
            self.assertEqual(appsensor_meta.cookie_dict, {"cookie-param": "value"})
            self.assertEqual(appsensor_meta.headers_dict, {"content-length": 100})
            self.assertEqual(appsensor_meta.json_dict, {"json-param": "value"})
            self.assertEqual(appsensor_meta.post_dict, {("post-param",): "value"})
            self.assertEqual(appsensor_meta.request_content_bytes_len, 100)
            self.assertEqual(
                appsensor_meta.files_dict,
                {("0", "filename-one",): "filename-one",
                 ("0", "filename-two",): "filename-two"}
            )
