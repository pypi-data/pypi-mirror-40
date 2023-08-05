# --------------------------------------------------------------------
# Copyright (c) iEXBase. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------

import functools

from tronapi.base.abi import (
    filter_by_name,
    filter_by_encodability,
    filter_by_argument_count,
    get_fallback_func_abi,
    abi_to_signature)

from tronapi.base.function_identifiers import FallbackFn
from tronapi.base.toolz import (
    pipe,
    valmap,
)
from tronapi.utils.types import is_text


def find_matching_fn_abi(abi, fn_identifier=None, args=None, kwargs=None):
    args = args or tuple()
    kwargs = kwargs or dict()
    filters = []
    num_arguments = len(args) + len(kwargs)
    diagnosis = None

    if fn_identifier is FallbackFn:
        return get_fallback_func_abi(abi)

    if not is_text(fn_identifier):
        raise TypeError("Unsupported function identifier")

    name_filter = functools.partial(filter_by_name, fn_identifier)
    arg_count_filter = functools.partial(filter_by_argument_count, num_arguments)
    encoding_filter = functools.partial(filter_by_encodability, args, kwargs)
    filters.extend([
        name_filter,
        arg_count_filter,
        encoding_filter,
    ])
    function_candidates = pipe(abi, *filters)
    if len(function_candidates) == 1:
        return function_candidates[0]
    else:
        matching_identifiers = name_filter(abi)
        matching_function_signatures = [abi_to_signature(func) for func in matching_identifiers]
        arg_count_matches = len(arg_count_filter(matching_identifiers))
        encoding_matches = len(encoding_filter(matching_identifiers))
        if arg_count_matches == 0:
            diagnosis = "\nFunction invocation failed due to improper number of arguments."
        elif encoding_matches == 0:
            diagnosis = "\nFunction invocation failed due to no matching argument types."
        elif encoding_matches > 1:
            diagnosis = (
                "\nAmbiguous argument encoding. "
                "Provided arguments can be encoded to multiple functions matching this call."
            )
        message = (
            "\nCould not identify the intended function with name `{name}`, "
            "positional argument(s) of type `{arg_types}` and "
            "keyword argument(s) of type `{kwarg_types}`."
            "\nFound {num_candidates} function(s) with the name `{name}`: {candidates}"
            "{diagnosis}"
        ).format(
            name=fn_identifier,
            arg_types=tuple(map(type, args)),
            kwarg_types=valmap(type, kwargs),
            num_candidates=len(matching_identifiers),
            candidates=matching_function_signatures,
            diagnosis=diagnosis,
        )
        raise ValueError(message)
