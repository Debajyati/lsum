from typing import Any, Tuple, Optional
import os
import pathspec

def assoclist(array1:list[Any], array2:list[Any]):
    result:list[Tuple[Any,Any]] = []

    length = min(len(array1),len(array2))
    for i in range(length):
        result.append((array1[i],array2[i]))
    return result

def get_gitignore_matcher(path: str) -> Optional[pathspec.PathSpec]:
    gitignore_path = os.path.join(path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
            return spec
    return None
