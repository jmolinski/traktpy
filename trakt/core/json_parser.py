from typing import Any, Dict, List

import jsons  # type: ignore
from trakt.core.exceptions import TraktResponseError

TYPE_TYPE = int.__class__
ITERABLES = {list, dict}


def parse_tree(data: Any, tree_structure: Any) -> Any:
    try:
        data = _substitute_none_val(data)
        return _parse_tree(data, tree_structure)
    except Exception as e:
        raise TraktResponseError(errors=[e])


def _substitute_none_val(data: Any):
    """Trakt represents null-value as {}. Change it to None."""
    if data == {}:
        return None

    if isinstance(data, list):
        data = [_substitute_none_val(v) for v in data]
    if isinstance(data, dict):
        data = {k: _substitute_none_val(v) for k, v in data.items()}

    return data


def _parse_tree(data: Any, tree_structure: Any) -> Any:
    level_type = tree_structure.__class__

    if level_type not in ITERABLES:
        return jsons.load(data, tree_structure)

    if level_type == list:
        return _parse_list(data, single_item_type=tree_structure[0])

    if level_type == dict:
        return _parse_dict(data, tree_structure)


def _is_arbitrary_value(x: Any) -> bool:
    return x.__class__ not in (ITERABLES | {type})


def _parse_list(data: List[Any], single_item_type: Any) -> List[Any]:
    if single_item_type is Any:
        return data
    if data is None:
        return []

    return [_parse_tree(e, single_item_type) for e in data]


def _parse_dict(data: Dict[Any, Any], tree_structure: Dict[Any, Any]) -> Dict[Any, Any]:
    wildcards = {  # eg {str: str} / {str: Any}
        k: v for k, v in tree_structure.items() if isinstance(k, type)
    }

    defaults = {  # eg {value: value}
        k: v
        for k, v in tree_structure.items()
        if (k not in wildcards) and _is_arbitrary_value(v)
    }

    result = dict()
    for k, v in data.items():
        if k in tree_structure:
            # v may be a default value -> use its type as subtree type
            subtree = tree_structure[k]
            subtree = subtree.__class__ if _is_arbitrary_value(subtree) else subtree

            result[k] = _parse_tree(v, subtree)
        elif k.__class__ in wildcards:
            wildcard = wildcards[k.__class__]
            result[k] = v if wildcard is Any else _parse_tree(v, wildcard)

    # set defaults if any keys are missing
    for k, v in defaults.items():
        if k not in result:
            result[k] = v

    return result
