from collections.abc import MutableMapping
from typing import List, Optional, Type, TypeVar, Union

T = TypeVar("T")


def flatten(d: dict, parent_key: str = "", sep: str = ":") -> dict:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten(d: dict, sep: str = ":") -> dict:
    res = dict()
    for key, value in d.items():
        parts = key.split(sep)
        d = res
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return res


def to_pythonic(data: dict) -> dict:
    flat_r = flatten(data)
    new_r = {}
    for k, v in flat_r.items():
        new_k = k.replace("-", "_")
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError:
                pass
        if new_k != k:
            new_r[new_k] = v
        else:
            new_r[k] = v
    data = unflatten(new_r)
    return data


def convert_to_model(
    data: Optional[Union[dict, list]], model: Type[T]
) -> Optional[Union[List[T], T]]:
    if isinstance(data, dict):
        data = to_pythonic(data)
        return model(**data)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            data[i] = to_pythonic(data[i])
        return [model(**i) for i in data]
    elif data is None:
        return None
