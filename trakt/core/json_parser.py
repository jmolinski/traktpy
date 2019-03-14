from typing import Any, Dict, List

import jsons

TYPE_TYPE = int.__class__
ITERABLES = {list, dict}


def parse_tree(data: Any, tree_structure: Any) -> Any:
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
    return [parse_tree(e, single_item_type) for e in data]


def _parse_dict(data: Dict[Any, Any], tree_structure: Dict[Any, Any]) -> Dict[Any, Any]:
    wildcards = {  # eg {str: str} / {str: value}
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
            # "normal" way

            # v may be default -> use its type as subtree
            subtree = tree_structure[k]
            subtree = subtree.__class__ if _is_arbitrary_value(subtree) else subtree

            result[k] = parse_tree(v, subtree)
        elif k.__class__ in wildcards:  # wildcard
            result[k] = parse_tree(v, wildcards[k.__class__])

    # set defaults if any is missing
    for k, v in defaults.items():
        if k not in result:
            result[k] = v

    return result
