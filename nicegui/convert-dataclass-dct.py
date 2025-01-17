from dataclasses import dataclass, asdict, is_dataclass
from typing import Any, Type, TypeVar
from tqdm.auto import tqdm
import json


T = TypeVar('T')

# Function to convert dataclass to dict


def dataclass_to_dict(instance: Any) -> dict:
    if not is_dataclass(instance):
        raise ValueError("Provided instance is not a dataclass")
    return asdict(instance)

# Function to convert dict to dataclass


def dict_to_dataclass(cls: Type[T], data: dict) -> T:
    if not is_dataclass(cls):
        raise ValueError("Provided class is not a dataclass")
    return cls(**data)

# Example usage


@dataclass(slots=True)
class Example:
    field1: int
    field2: str

    def add(self, i=1):
        self.field1 += i


class ExtendedExample(Example):
    def __init__(self, dct: dict):
        super().__init__(**dct)

    @property
    def as_dict(self):
        return asdict(self)

    @property
    def as_str(self):
        return json.dumps(self.as_dict)


ee = ExtendedExample(dict(field1=1, field2='field2'))
print(ee)
print(type(ee.as_dict), ee.as_dict)
print(type(ee.as_str), ee.as_str)
ee.add()
print(ee)

input_dict = dict(field1=1, field2='example')
num = int(1e5)
for _ in tqdm(range(num), 'dict to cls'):
    ee = ExtendedExample(input_dict)

for _ in tqdm(range(num), 'cls to dict'):
    d = ee.as_dict

for _ in tqdm(range(num), 'cls to str'):
    s = ee.as_str

for _ in tqdm(range(num), 'loads(str)'):
    json.loads(s)

for _ in tqdm(range(num), 'dumps(dict)'):
    json.dumps(d)

# example_instance = Example(field1=1, field2="example")

# for _ in tqdm(range(10000), 'cls to dict'):
#     example_dict = dataclass_to_dict(example_instance)
# print(example_dict)

# # Convert example_dict to JSON string
# for _ in tqdm(range(10000), 'dict to str'):
#     example_json = json.dumps(example_dict)
# print(example_json)

# # Convert JSON string back to dict
# for _ in tqdm(range(10000), 'str to dict'):
#     example_dict_from_json = json.loads(example_json)
# print(example_dict_from_json)

# # Convert example_dict to and from json str
# for _ in tqdm(range(10000), 'dict to cls'):
#     new_instance = dict_to_dataclass(Example, example_dict_from_json)
# print(new_instance)
