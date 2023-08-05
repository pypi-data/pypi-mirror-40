from typing import Iterable, Union, List


def head(obj: Union[Iterable, List[any]]):
    try:
        return obj[0] if obj else None
    except (KeyError, TypeError):
        return None
