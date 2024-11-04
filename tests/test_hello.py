import pytest

from src.hello import main
from typing import Callable


@pytest.fixture(scope="function")
def hello() -> Callable:
    return main()


def test_hello(hello) -> None:
    assert hello == "world"
