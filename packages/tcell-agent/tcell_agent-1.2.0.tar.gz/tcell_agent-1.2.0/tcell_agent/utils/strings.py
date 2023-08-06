from tcell_agent.utils.compat import a_string


def ensure_str_or_unicode(encoding, value):
    if isinstance(value, bytes):
        try:
            return value.decode(encoding)
        except UnicodeDecodeError:
            return value.decode("ISO-8859-1")
    else:
        return value


def ensure_string(value):
    if a_string(value):
        return ensure_str_or_unicode("utf-8", value)

    return str(value)
