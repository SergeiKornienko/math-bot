"""Tests for the tokenizer module."""

from decimal import Decimal

import pytest

from core.exceptions import TokenizerError
from core.tokenizer import tokenize


def test_single_integer():
    """A single integer is tokenized to a list with one Decimal."""
    assert tokenize("42") == [Decimal("42")]


def test_single_decimal():
    """A decimal number is tokenized correctly."""
    assert tokenize("3.14") == [Decimal("3.14")]


def test_leading_decimal_point():
    """A number starting with a decimal point, like .5, is parsed as 0.5."""
    assert tokenize(".5") == [Decimal("0.5")]


def test_addition():
    """Simple addition: numbers and operator."""
    assert tokenize("2+3") == [Decimal("2"), "+", Decimal("3")]


def test_spaces_are_ignored():
    """Spaces between tokens are skipped."""
    assert tokenize(" 2 + 3 ") == [Decimal("2"), "+", Decimal("3")]


def test_mixed_expression():
    """Expression with multiple operators and parentheses."""
    assert tokenize("12 + 3.14 * (2 - 5)") == [
        Decimal("12"),
        "+",
        Decimal("3.14"),
        "*",
        "(",
        Decimal("2"),
        "-",
        Decimal("5"),
        ")"
    ]


def test_unary_minus_at_start():
    """Unary minus at the beginning of an expression."""
    assert tokenize("-5") == ["-", Decimal("5")]


def test_unary_minus_after_operator():
    """Unary minus after an operator."""
    assert tokenize("2 * -3") == [Decimal("2"), "*", "-", Decimal("3")]


def test_unary_minus_after_parenthesis():
    """Unary minus after an opening parenthesis."""
    assert tokenize("(-5)") == ["(", "-", Decimal("5"), ")"]


def test_all_operators():
    """All supported operators are tokenized."""
    assert tokenize("+-*/()") == ["+", "-", "*", "/", "(", ")"]


def test_unknown_symbol_raises_error():
    """An unknown symbol raises TokenizerError."""
    with pytest.raises(TokenizerError, match="unknown symbol"):
        tokenize("2 @ 3")


def test_empty_string():
    """Empty string returns an empty list."""
    assert tokenize("") == []
