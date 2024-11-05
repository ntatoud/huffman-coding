import pytest
from src.binary_code import (
    BinaryCode,
    Bit,
    AtLeastOneBitError,
)


@pytest.fixture(scope="function")
def binary_code_with_one():
    return BinaryCode(Bit.ONE)


@pytest.fixture(scope="function")
def binary_code_with_zero():
    return BinaryCode(Bit.ZERO)


@pytest.fixture(scope="function")
def binary_code_with_zero_one():
    return BinaryCode(Bit.ZERO, Bit.ONE)


@pytest.fixture(scope="function")
def binary_code_with_one_zero_one():
    return BinaryCode(Bit.ONE, Bit.ZERO, Bit.ONE)


def test_initialization_should_pass(binary_code_with_one):
    # With one bit
    assert str(binary_code_with_one) == "1"

    # With multiple bits
    code = BinaryCode(Bit.ONE, Bit.ZERO, Bit.ONE)
    assert str(code) == "101"


def test_add_bits_should_pass(binary_code_with_zero):
    binary_code_with_zero.add(Bit.ONE)
    assert str(binary_code_with_zero) == "01"

    binary_code_with_zero.add(Bit.ZERO)
    assert str(binary_code_with_zero) == "010"


def test_add_bit_should_fail(binary_code_with_zero):
    with pytest.raises(TypeError):
        binary_code_with_zero.add("A")


def test_bits_property(binary_code_with_zero_one):
    assert binary_code_with_zero_one.bits == [Bit.ZERO, Bit.ONE]


def test_getitem():
    # Test getting a bit by index
    code = BinaryCode(Bit.ZERO, Bit.ONE, Bit.ZERO)
    assert str(code[0]) == "0"
    assert str(code[1]) == "1"

    # Test getting a slice of bits
    sub_code = code[1:]
    assert str(sub_code) == "10"

    sub_code = code[:2]
    assert str(sub_code) == "01"


def test_setitem(binary_code_with_zero_one):
    # Test setting a bit at a specific index
    binary_code_with_zero_one[1] = Bit.ZERO
    assert str(binary_code_with_zero_one) == "00"


def test_delitem(binary_code_with_zero_one):
    del binary_code_with_zero_one[1]
    assert str(binary_code_with_zero_one) == "0"

    # Test deleting the last remaining bit raises an error
    with pytest.raises(AtLeastOneBitError):
        del binary_code_with_zero_one[0]


def test_len(binary_code_with_one_zero_one):
    # Test the length of BinaryCode
    assert len(binary_code_with_one_zero_one) == 3

    # Test length after modification
    del binary_code_with_one_zero_one[1]
    assert len(binary_code_with_one_zero_one) == 2


def test_equality(binary_code_with_zero_one):
    # Test equality of two BinaryCode instances
    assert binary_code_with_zero_one == BinaryCode(Bit.ZERO, Bit.ONE)

    code1 = BinaryCode(Bit.ONE, Bit.ONE)
    assert binary_code_with_zero_one != code1

    code2 = BinaryCode(Bit.ONE)
    assert binary_code_with_zero_one != code2


def test_iteration(binary_code_with_one_zero_one):
    # Test iteration over bits
    bits = [bit for bit in binary_code_with_one_zero_one]
    assert bits == [Bit.ONE, Bit.ZERO, Bit.ONE]


def test_repr_and_str(binary_code_with_one_zero_one):
    # Test the __repr__ and __str__ methods
    assert repr(binary_code_with_one_zero_one) == "BinaryCode(101)"
    assert str(binary_code_with_one_zero_one) == "101"


def test_hash(binary_code_with_one_zero_one):
    # Test the __hash__ method
    code = binary_code_with_one_zero_one
    code2 = binary_code_with_one_zero_one

    assert hash(code) == hash(code2)
    assert hash(code) == hash("101")
