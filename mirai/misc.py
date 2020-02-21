from enum import Enum
import asyncio
from threading import Thread, Lock
import typing as T

def assertOperatorSuccess(result, raise_exception=False, return_as_is=False):
    if "code" in result:
        if not raise_exception:
            return result['code'] == 0
        else:
            if result['code'] != 0:
                raise ValueError(f"""invaild stdin: { {
                    1: "wrong auth key",
                    2: "unknown qq account",
                    3: "invaild session key",
                    4: "disabled session key",
                    5: "unknown receiver target",
                    10: "permission denied",
                    400: "wrong arguments"
                }[result['code']] }""")
            else:
                if return_as_is:
                    return result
                else:
                    return True
    if return_as_is:
        return result
    return False

class ImageType(Enum):
    Friend = "friend"
    Group = "group"

ImageRegex = {
    "group": r"(?<=\{)([0-9A-Z]{8})\-([0-9A-Z]{4})-([0-9A-Z]{4})-([0-9A-Z]{4})-([0-9A-Z]{12})(?=\}\.jpg)",
    "friend": r"(?<=/)([0-9a-z]{8})\-([0-9a-z]{4})-([0-9a-z]{4})-([0-9a-z]{4})-([0-9a-z]{12})"
}

def findKey(mapping, value):
    index = list(mapping.values()).index(value)
    return list(mapping.keys())[index]

def raiser(error):
    raise error

def printer(val):
    print(val)
    return val