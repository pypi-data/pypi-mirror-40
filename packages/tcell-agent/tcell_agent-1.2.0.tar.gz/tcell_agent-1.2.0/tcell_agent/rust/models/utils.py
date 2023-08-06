from future.utils import iteritems
from tcell_agent.converters.params import flatten_clean


def convert_params(encoding, params_dict, need_to_flatten=True):
    if params_dict is None:
        return []

    flattened_dict = params_dict
    if need_to_flatten:
        flattened_dict = flatten_clean(encoding, params_dict)

    flattened_params = []
    for param_name, param_value in iteritems(flattened_dict):
        flattened_params.append({"name": param_name[-1], "value": param_value})

    return flattened_params
