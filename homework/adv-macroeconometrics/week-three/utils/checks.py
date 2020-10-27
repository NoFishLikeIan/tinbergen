from typing import List, Any

def is_uniq(group: List[Any]) -> bool:

    seen = set()

    for elem in group:
        if elem in seen: 
            return False

        seen.add(elem)

    return True