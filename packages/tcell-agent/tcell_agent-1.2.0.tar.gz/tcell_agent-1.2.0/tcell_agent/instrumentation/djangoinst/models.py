from tcell_agent.instrumentation.headers_cleaner import headers_from_environ


class TCellDjangoRequest(object):
    def __init__(self, request):
        try:
            self.content_length = int(
                request.META.get("CONTENT_LENGTH", 0)
            )
        except Exception:
            self.content_length = 0

        self.normalized_headers = headers_from_environ(request.META)

        self.filenames_dict = {}
        for param_name in (request.FILES or {}).keys():
            self.filenames_dict[param_name] = []
            for file_obj in request.FILES.getlist(param_name):
                self.filenames_dict[param_name].append(file_obj.name)


class TCellDjangoContentType(object):
    def __init__(self, request):
        self.content_type = request.META.get(
            "CONTENT_TYPE", ""
        ).lower()

    def is_multipart(self):
        self.content_type.startswith("multipart/form-data")
