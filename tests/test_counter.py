from src.counter import Counter
from pytest import fixture, mark


@fixture(scope="function")
def counter():
    return Counter({"a": 2, "b": 3})


@fixture(scope="function")
def counter2():
    return Counter({"a": 1, "b": 2, "c": 3, "d": 1, "e": 3})


def test_elements(counter2):
    assert counter2.elements() == {"a", "b", "c", "d", "e"}


@mark.parametrize(
    "element, occurences",
    [("a", 2), ("b", 3), ("c", 0)],
)
def test_nb_occurrences(counter, element, occurences):
    counter.set_nb_occurences(element, occurences)
    assert counter.get_nb_occurences(element) == occurences


@mark.parametrize(
    "element, increased_occurences",
    [("a", 3), ("b", 4)],
)
def test_increase(counter, element, increased_occurences):
    counter.increase(element)
    assert counter.get_nb_occurences(element) == increased_occurences


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


def test_should_not_be_equal(counter):
    assert counter != Counter({"a": 2, "b": 1})
