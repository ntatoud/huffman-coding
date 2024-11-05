#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytest

from src.huffman_tree import (
    HuffmanTree,
    IncoherentHuffmanTreeError,
    MustBeALeafError,
    MustNotBeALeafError,
)


@pytest.fixture(scope="function")
def leaf():
    return HuffmanTree("a", 1)


@pytest.fixture(scope="function")
def leaf2():
    return HuffmanTree("a", 1)


@pytest.fixture(scope="function")
def leaf3():
    return HuffmanTree("b", 2)


@pytest.fixture(scope="function")
def tree():
    return HuffmanTree(left_child=HuffmanTree("a", 1), right_child=HuffmanTree("b", 2))


@pytest.fixture(scope="function")
def tree2():
    return HuffmanTree(left_child=HuffmanTree("a", 1), right_child=HuffmanTree("b", 2))


@pytest.fixture(scope="function")
def tree3():
    return HuffmanTree(left_child=HuffmanTree("b", 2), right_child=HuffmanTree("a", 1))


def test_incoherent_huffman_tree_error_empty_tree():
    with pytest.raises(IncoherentHuffmanTreeError):
        HuffmanTree()


def test_incoherent_huffman_tree_error_equal_children(leaf):
    with pytest.raises(IncoherentHuffmanTreeError):
        HuffmanTree(left_child=leaf, right_child=leaf)


@pytest.mark.parametrize("ab, result", [("leaf", True), ("tree", False)])
def test_is_leaf(ab, result, request):
    assert request.getfixturevalue(ab).is_leaf == result


def test_must_be_a_leaf_error(tree):
    with pytest.raises(MustBeALeafError):
        tree.element


def test_element(leaf):
    assert leaf.element == "a"


@pytest.mark.parametrize("ab, result", [("leaf", 1), ("tree", 3)])
def test_nb_occurrences(ab, result, request):
    assert request.getfixturevalue(ab).nb_occurrences == result


def test_mus_not_be_a_leaf_error(leaf):
    with pytest.raises(MustNotBeALeafError):
        leaf.left_child

    with pytest.raises(MustNotBeALeafError):
        leaf.right_child


@pytest.mark.parametrize(
    "ab1, ab2, result",
    [
        ("leaf", "leaf2", True),
        ("leaf", "leaf3", False),
        ("tree", "tree2", True),
        ("tree", "tree3", False),
        ("leaf", "tree", False),
        ("tree", "leaf", False),
    ],
)
def test_equivalent(ab1, ab2, result, request):
    assert (
        request.getfixturevalue(ab1).equivalent(request.getfixturevalue(ab2))
    ) == result


def test_equivalent_with_non_huffman_tree(leaf):
    with pytest.raises(AttributeError):
        leaf.equivalent("hello")


def test_left_child(tree, leaf):
    assert tree.left_child.equivalent(leaf)


def test_right_child(tree, leaf3):
    assert tree.right_child.equivalent(leaf3)


def test_add_should_pass(tree, leaf, leaf3):
    assert tree.equivalent(leaf + leaf3)


@pytest.mark.parametrize(
    "ab1, ab2, result",
    [
        ("leaf", "leaf2", False),
        ("leaf", "leaf3", True),
        ("leaf", "tree", True),
    ],
)
def test_lower_than(ab1, ab2, result, request):
    assert (request.getfixturevalue(ab1) < request.getfixturevalue(ab2)) == result


@pytest.mark.parametrize(
    "ab1, ab2, result",
    [
        ("leaf", "leaf2", True),
        ("leaf", "leaf3", True),
        ("leaf", "tree", True),
    ],
)
def test_lower_than_or_equal(ab1, ab2, result, request):
    assert (request.getfixturevalue(ab1) <= request.getfixturevalue(ab2)) == result


@pytest.mark.parametrize(
    "ab1, ab2, result",
    [
        ("leaf", "leaf2", False),
        ("leaf", "leaf3", False),
        ("tree", "leaf", True),
    ],
)
def test_greater_than(ab1, ab2, result, request):
    assert (request.getfixturevalue(ab1) > request.getfixturevalue(ab2)) == result


@pytest.mark.parametrize(
    "ab1, ab2, result",
    [
        ("leaf", "leaf2", True),
        ("leaf", "leaf3", False),
        ("tree", "leaf", True),
    ],
)
def test_greater_than_or_equal(ab1, ab2, result, request):
    assert (request.getfixturevalue(ab1) >= request.getfixturevalue(ab2)) == result


@pytest.mark.parametrize(
    "huffman_tree, result",
    [("leaf", "(1, a)"), ("tree", "(3, (1, a),  (2, b))")],
)
def test_str(huffman_tree, result, request):
    assert str(request.getfixturevalue(huffman_tree)) == result


@pytest.mark.parametrize(
    "huffman_tree, result",
    [
        ("leaf", "HuffmanTree(element=a, nb_occurrences=1)"),
        (
            "tree",
            "HuffmanTree(nb_occurrences=3, left_child=HuffmanTree(element=a, nb_occurrences=1), right_child=HuffmanTree(element=b, nb_occurrences=2))",
        ),
    ],
)
def test_repr(huffman_tree, result, request):
    assert repr(request.getfixturevalue(huffman_tree)) == result
