from tcell_agent.rust.models.utils import convert_params


class PatchesRequest(dict):
    def __init__(self, appsensor_meta):
        dict.__init__(self)
        json_dict = appsensor_meta.json_dict or {}
        if not isinstance(json_dict, dict):
            json_dict = {"body": json_dict}
        post_params = convert_params(appsensor_meta.encoding, appsensor_meta.post_dict, False) + \
            convert_params(appsensor_meta.encoding, appsensor_meta.files_dict, False) + \
            convert_params(appsensor_meta.encoding, json_dict)

        self["full_uri"] = appsensor_meta.location
        self["method"] = appsensor_meta.method
        self["path"] = appsensor_meta.path
        self["remote_address"] = appsensor_meta.remote_address
        self["request_bytes_length"] = appsensor_meta.request_content_bytes_len
        self["query_params"] = convert_params(appsensor_meta.encoding, appsensor_meta.get_dict)
        self["post_params"] = post_params
        self["headers"] = convert_params(appsensor_meta.encoding, appsensor_meta.headers_dict)
        self["cookies"] = convert_params(appsensor_meta.encoding, appsensor_meta.cookie_dict)
