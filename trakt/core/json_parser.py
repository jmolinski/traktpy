from copy import deepcopy

import jsons

TYPE_TYPE = int.__class__
ITERABLES = [list, dict]


def parse_tree(data, tree_structure):
    if not tree_structure:
        return deepcopy(tree_structure)

    level_type = tree_structure.__class__

    if level_type not in ITERABLES:
        return jsons.load(data, tree_structure)

    result = level_type()

    if level_type == list:
        subtree = tree_structure[0]
        for e in data:
            parsed = parse_tree(e, subtree)
            result.append(parsed)

    if level_type == dict:
        for k, v in data.items():
            if k not in tree_structure:
                continue

            subtree = tree_structure[k]
            result[k] = parse_tree(v, subtree)

    return result
