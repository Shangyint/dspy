# Note(shangyin): What abstractions we want to make about assertions?
# things to consider: what we want to assert, and what would be the syntax?
# One possible starting point would be constraints on the output of a module
from typing import Any
import dspy

# compile time assertion
class Assert:
    def __init__(self, assert_fun, *args, **kwargs):
        self.assert_fun = assert_fun
        self.args = args
        self.kwargs = kwargs

    # assert fun should always return bool
    def __call__(self) -> bool:
        result = self.assert_fun(*self.args, **self.kwargs)
        if isinstance(result, bool):
            if result:
                return True
            else:
                raise AssertionError(f"Assertion {self.assert_fun} failed")
        else:
            raise ValueError("Assertion function should always return [bool]")
        
# we could possibly to have runtime assertions as well
# class RuntimeAssert(Assert): ...


class Assertions(dspy.Module):
    def __init__(self) -> None:
        self.assertions = []
    
    def add(self, assertion: Assert):
        self.assertions.append(assertion)

    def __call__(self, assertion: Assert):
        self.add(assertion)
        if self._compiled:
            return True
        else:
            return assertion()

def assert_transform(backtrack=2):
    def wrapper(func):
        def inner(*args, **kwargs):
            for i in range(backtrack):
                try:
                    return func(*args, **kwargs)
                except AssertionError as e:
                    # Add metadata to state
                    pass
        return inner 
    return wrapper
    