import pytest

from src.priority_queue import (
    ElementNotComparableError,
    PriorityQueue,
    PriorityQueueEmptyError,
)


@pytest.fixture(scope="function")
def empty_queue():
    return PriorityQueue()


@pytest.fixture(scope="function")
def non_empty_queue():
    return PriorityQueue((2, 1, 4, 3, 5))


@pytest.fixture(scope="function")
def non_empty_queue2():
    return PriorityQueue((2, 1, 4, 3, 5))


@pytest.fixture(scope="function")
def non_empty_queue3():
    return PriorityQueue((2, 1, 4, 3, 6))


@pytest.mark.parametrize(
    "priority_queue, expected",
    [("empty_queue", True), ("non_empty_queue", False)],
)
def test_is_empty(priority_queue, expected, request):
    assert request.getfixturevalue(priority_queue).is_empty == expected


@pytest.mark.parametrize(
    "priority_queue_one, priority_queue_two, expected",
    [
        ("empty_queue", "empty_queue", True),
        ("empty_queue", "non_empty_queue", False),
        ("non_empty_queue", "non_empty_queue2", True),
        ("non_empty_queue", "non_empty_queue3", False),
    ],
)
def test_are_equal(priority_queue_one, priority_queue_two, expected, request):
    assert (
        request.getfixturevalue(priority_queue_one)
        == request.getfixturevalue(priority_queue_two)
    ) == expected


def test_append_then_pop_with_higher_priority(non_empty_queue, non_empty_queue2):
    non_empty_queue2.append(0)
    non_empty_queue2.pop()
    assert non_empty_queue == non_empty_queue2


def test_append_then_pop_with_lower_priority(non_empty_queue):
    non_empty_queue.append(4)
    non_empty_queue.pop()
    assert non_empty_queue == PriorityQueue((4, 2, 4, 3, 5))


def test_append_highest_priority_element(non_empty_queue):
    non_empty_queue.append(0)
    assert non_empty_queue.element == 0


@pytest.mark.parametrize(
    "priority_queue, expected",
    [
        ("empty_queue", "PriorityQueue()"),
        ("non_empty_queue", "PriorityQueue(1, 2, 3, 4, 5)"),
    ],
)
def test_repr(priority_queue, expected, request):
    assert repr(request.getfixturevalue(priority_queue)) == expected


@pytest.mark.parametrize(
    "priority_queue, expected",
    [
        ("empty_queue", ""),
        ("non_empty_queue", "1, 2, 3, 4, 5"),
    ],
)
def test_str(priority_queue, expected, request):
    assert str(request.getfixturevalue(priority_queue)) == expected


def test_element_should_raise_empty_error(empty_queue):
    with pytest.raises(PriorityQueueEmptyError):
        empty_queue.element


def test_pop_should_raise_empty_error(empty_queue):
    with pytest.raises(PriorityQueueEmptyError):
        empty_queue.pop()


@pytest.mark.parametrize(
    "priority_queue, element",
    [
        ("empty_queue", {}),
        ("non_empty_queue", "a"),
    ],
)
def test_append_should_raise_not_comparable_error(priority_queue, element, request):
    with pytest.raises(ElementNotComparableError):
        request.getfixturevalue(priority_queue).append(element)
