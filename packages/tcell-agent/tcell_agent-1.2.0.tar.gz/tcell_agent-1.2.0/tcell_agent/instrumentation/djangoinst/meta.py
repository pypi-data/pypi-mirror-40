import json
import uuid

from tcell_agent.converters.params import flatten_clean
from tcell_agent.global_state import get_default_charset
from tcell_agent.instrumentation.better_ip_address import better_ip_address
from tcell_agent.instrumentation.context import TCellInstrumentationContext
from tcell_agent.instrumentation.decorators import catches_generic_exception
from tcell_agent.instrumentation.djangoinst.routes import get_route_id
from tcell_agent.instrumentation.djangoinst.models import \
     TCellDjangoRequest, TCellDjangoContentType
from tcell_agent.utils.strings import ensure_str_or_unicode

MAXIMUM_BODY_SIZE = 2000000


@catches_generic_exception(__name__, "Error setting request context information")
def initialize_tcell_context(request):
    request._tcell_context = TCellInstrumentationContext()
    request._tcell_context.transaction_id = str(uuid.uuid4())
    request._tcell_context.referrer = request.META.get("HTTP_REFERER")
    request._tcell_context.user_agent = request.META.get("HTTP_USER_AGENT")
    request._tcell_context.remote_address = better_ip_address(request.META)
    request._tcell_context.method = request.method
    request._tcell_context.path = request.path
    request._tcell_context.fullpath = request.get_full_path()
    request._tcell_context.uri = request.build_absolute_uri()
    request._tcell_context.route_id = get_route_id(request)


def get_appsensor_meta(request):
    appsensor_meta = request._tcell_context.appsensor_meta
    appsensor_meta.remote_address = request._tcell_context.remote_address
    appsensor_meta.method = request._tcell_context.method
    appsensor_meta.user_agent_str = request._tcell_context.user_agent
    appsensor_meta.location = request._tcell_context.uri
    appsensor_meta.path = request._tcell_context.path
    appsensor_meta.route_id = request._tcell_context.route_id
    appsensor_meta.session_id = request._tcell_context.session_id
    appsensor_meta.user_id = request._tcell_context.user_id
    appsensor_meta.encoding = request.encoding or get_default_charset()

    return appsensor_meta


def set_response(meta, django_response_class, response):
    if meta.response_processed:
        return
    meta.response_processed = True

    response_content_len = 0
    try:
        if isinstance(response, django_response_class):
            response_content_len = len(response.content)
    except Exception:
        pass

    meta.response_content_bytes_len = response_content_len
    meta.response_code = response.status_code


def check_body_for_json(post_dict, request_body, encoding):
    if len(request_body) >= MAXIMUM_BODY_SIZE:
        return [post_dict, {}]

    request_body = ensure_str_or_unicode(encoding, request_body)
    if request_body[0] == "{" or request_body[0] == "[":
        try:
            return [{}, json.loads(request_body)]
        except ValueError:
            pass

    return [post_dict, {}]


def parse_body(request, content_length, encoding):
    post_dict = request.POST

    if (not content_length) or content_length >= MAXIMUM_BODY_SIZE:
        return [post_dict, {}]

    content_type = TCellDjangoContentType(request)
    if content_type.is_multipart():
        return [post_dict, {}]

    return check_body_for_json(post_dict, request.body, encoding)


def set_request(meta, request):
    if meta.request_processed:
        return
    meta.request_processed = True

    django_request = TCellDjangoRequest(request)
    post_dict, json_dict = parse_body(request,
                                      django_request.content_length,
                                      meta.encoding)
    meta.get_dict = request.GET
    meta.cookie_dict = request.COOKIES
    meta.headers_dict = django_request.normalized_headers
    meta.json_dict = json_dict
    meta.request_content_bytes_len = django_request.content_length
    meta.files_dict = flatten_clean(meta.encoding,
                                    django_request.filenames_dict)
    meta.post_dict = flatten_clean(meta.encoding, post_dict)
