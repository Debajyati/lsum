from typing import Any, Tuple

def assoclist(array1:list[Any], array2:list[Any]):
    result:list[Tuple[Any,Any]] = []

    length = min(len(array1),len(array2))
    for i in range(length):
        result.append((array1[i],array2[i]))
    return result
