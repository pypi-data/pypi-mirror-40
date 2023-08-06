from future.utils import iteritems


def headers_from_environ(environ):
    include = ("content-length", "content-type")
    exclude = ("http-cookie")

    env = environ or {}

    env_low_hyphen = {header_name.lower().replace("_", "-"): header_value
                      for header_name, header_value in iteritems(env)}

    env_filtered = {header_name: header_value
                    for header_name, header_value in iteritems(env_low_hyphen)
                    if header_name.startswith("http-") or header_name in include
                    if header_name not in exclude}

    env_deprefixed = {
        header_name[5:] if header_name.startswith("http-") else header_name:
        header_value
        for header_name, header_value in iteritems(env_filtered)
    }

    return env_deprefixed
