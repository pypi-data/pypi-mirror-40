from future.utils import iteritems

from tcell_agent.converters.params import flatten_clean
from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.instrumentation.better_ip_address import better_ip_address
from tcell_agent.instrumentation.context import TCellInstrumentationContext
from tcell_agent.instrumentation.decorators import catches_generic_exception
from tcell_agent.instrumentation.headers_cleaner import headers_from_environ
from tcell_agent.features.request_timing import start_timer


@catches_generic_exception(__name__, "Error initializing Flask context")
def initialize_tcell_context(request):
    from tcell_agent.instrumentation.flaskinst.routes import calculate_route_id

    request._tcell_context = TCellInstrumentationContext()

    request._tcell_context.method = request.environ.get("REQUEST_METHOD")
    if request.url_rule is not None:
        request._tcell_context.route_id = calculate_route_id(request._tcell_context.method,
                                                             request.url_rule.rule)
    request._tcell_context.user_agent = request.environ.get("HTTP_USER_AGENT")
    request._tcell_context.remote_address = better_ip_address(request.environ)
    request._tcell_context.uri = request.url
    request._tcell_context.path = request.path
    request._tcell_context.fullpath = request.full_path

    start_timer(request)

    # run this here to ensure variables required by process_response are set
    # before calling letting the request processing continue in case
    # an exception is raised
    request._appsensor_meta = AppSensorMeta()
    request._ip_blocking_triggered = False


@catches_generic_exception(__name__, "Error initializing Flask meta")
def create_meta(request):
    appsensor_meta = AppSensorMeta()
    request._appsensor_meta = appsensor_meta
    appsensor_meta.remote_address = request._tcell_context.remote_address
    appsensor_meta.method = request.environ.get("REQUEST_METHOD")
    appsensor_meta.user_agent_str = request._tcell_context.user_agent
    appsensor_meta.location = request.url
    appsensor_meta.path = request.path
    appsensor_meta.route_id = request._tcell_context.route_id

    appsensor_meta.get_dict = request.args
    appsensor_meta.cookie_dict = request.cookies
    appsensor_meta.headers_dict = headers_from_environ(request.environ)
    try:
        appsensor_meta.json_dict = request.json or {}
    except Exception:
        appsensor_meta.json_dict = None
    appsensor_meta.request_content_bytes_len = request.content_length or 0

    appsensor_meta.post_dict = flatten_clean(request.charset, request.form)
    appsensor_meta.path_dict = request.view_args

    files_dict = {}
    for param_name, file_obj in iteritems(request.files or {}):
        files_dict[param_name] = file_obj.filename

    appsensor_meta.files_dict = flatten_clean(request.charset, files_dict)


def update_meta_with_response(appsensor_meta, response, response_code):
    appsensor_meta.response_code = response_code
    if response is not None:
        appsensor_meta.response_content_bytes_len = response.content_length or 0
