from src.counter import Counter
from pytest import fixture, mark


@fixture(scope="function")
def empty_counter():
    return Counter()


@fixture(scope="function")
def counter():
    return Counter({"a": 2, "b": 3})


@fixture(scope="function")
def counter2():
    return Counter({"a": 1, "b": 2, "c": 3, "d": 1, "e": 3})


def test_elements(counter2):
    assert counter2.elements == {"a", "b", "c", "d", "e"}


@mark.parametrize(
    "element, occurences",
    [("a", 2), ("b", 3), ("c", 0)],
)
def test_nb_occurrences(counter, element, occurences):
    counter.set_nb_occurences(element, occurences)
    assert counter.get_nb_occurences(element) == occurences


@mark.parametrize(
    "some_counter, element, increased_occurences",
    [("empty_counter", "a", 1), ("counter", "a", 3), ("counter", "b", 4)],
)
def test_increase(some_counter, element, increased_occurences, request):
    actual_counter = request.getfixturevalue(some_counter)
    actual_counter.increase(element)
    assert actual_counter.get_nb_occurences(element) == increased_occurences


def test_least_frequent_elements(counter2):
    assert counter2.least_frequent_elements() == {"a", "d"}


def test_most_frequent_elements(counter2):
    assert counter2.most_frequent_elements() == {"c", "e"}


def test_elements_by_occurence(counter2):
    assert counter2.elements_by_occurence() == {1: {"a", "d"}, 2: {"b"}, 3: {"c", "e"}}


def test_str(counter):
    assert str(counter) == "{'a': 2, 'b': 3}"


def test_repr(counter):
    assert repr(counter) == "Counter({'a': 2, 'b': 3})"


def test_should_be_equal(counter):
    assert counter == Counter({"a": 2, "b": 3})


@mark.parametrize(
    "other",
    [Counter({"a": 2, "b": 1}), "invalid"],
)
def test_should_not_be_equal(counter, other):
    assert counter != other
