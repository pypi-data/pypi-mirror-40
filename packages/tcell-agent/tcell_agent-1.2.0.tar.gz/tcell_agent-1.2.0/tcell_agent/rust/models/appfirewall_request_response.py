from tcell_agent.rust.models.utils import convert_params


class AppfirewallRequestResponse(dict):
    def __init__(self, appsensor_meta):
        dict.__init__(self)
        json_dict = appsensor_meta.json_dict or {}
        if not isinstance(json_dict, dict):
            json_dict = {"body": json_dict}
        post_params = convert_params(appsensor_meta.encoding, appsensor_meta.post_dict, False) + \
            convert_params(appsensor_meta.encoding, appsensor_meta.files_dict, False) + \
            convert_params(appsensor_meta.encoding, json_dict)

        self["method"] = appsensor_meta.method
        self["status_code"] = appsensor_meta.response_code
        self["route_id"] = appsensor_meta.route_id
        self["path"] = appsensor_meta.path
        self["query_params"] = convert_params(appsensor_meta.encoding, appsensor_meta.get_dict)
        self["post_params"] = post_params
        self["headers"] = convert_params(appsensor_meta.encoding, appsensor_meta.headers_dict)
        self["cookies"] = convert_params(appsensor_meta.encoding, appsensor_meta.cookie_dict)
        self["path_params"] = convert_params(appsensor_meta.encoding, appsensor_meta.path_dict)
        self["remote_address"] = appsensor_meta.remote_address
        self["full_uri"] = appsensor_meta.location
        self["session_id"] = appsensor_meta.session_id
        self["user_id"] = appsensor_meta.user_id
        self["user_agent"] = appsensor_meta.user_agent_str
        self["request_bytes_length"] = appsensor_meta.request_content_bytes_len
        self["response_bytes_length"] = appsensor_meta.response_content_bytes_len
        self["sql_exceptions"] = appsensor_meta.sql_exceptions
        self["database_result_sizes"] = appsensor_meta.database_result_sizes

        if appsensor_meta.csrf_reason:
            self["csrf_exception"] = {"exception_payload": appsensor_meta.csrf_reason}
