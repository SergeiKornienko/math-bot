"""Tests for the Shunting-yard parser."""

from decimal import Decimal

import pytest

from core.exceptions import ParsingError
from core.parser import to_postfix
from core.tokenizer import tokenize


def parse(expr: str):
    """Helper: tokenize then parse to postfix."""
    return to_postfix(tokenize(expr))


def test_single_number():
    """A single number returns just that number."""
    assert parse("42") == [Decimal("42")]


def test_simple_addition():
    """2 + 3 -> 2 3 +"""
    assert parse("2 + 3") == [Decimal("2"), Decimal("3"), "+"]


def test_operator_precedence():
    """2 + 3 * 4 -> 2 3 4 * +"""
    assert parse("2 + 3 * 4") == [
        Decimal("2"),
        Decimal("3"),
        Decimal("4"),
        "*",
        "+",
    ]


def test_parentheses():
    """(2 + 3) * 4 -> 2 3 + 4 *"""
    assert parse("(2 + 3) * 4") == [
        Decimal("2"),
        Decimal("3"),
        "+",
        Decimal("4"),
        "*",
    ]


def test_nested_parentheses():
    """((2 + 3)) -> 2 3 +"""
    assert parse("((2 + 3))") == [
        Decimal("2"),
        Decimal("3"),
        "+",
    ]


def test_unary_minus():
    """-5 + 3 -> 5 unary- 3 +"""
    result = parse("-5 + 3")
    assert result == [
        Decimal("5"),
        "u-",
        Decimal("3"),
        "+",
    ]


def test_unary_minus_in_parentheses():
    """(-5) -> 5 unary-"""
    assert parse("(-5)") == [Decimal("5"), "u-"]


def test_unary_minus_with_multiplication():
    """2 * -3 -> 2 3 unary- *"""
    assert parse("2 * -3") == [
        Decimal("2"),
        Decimal("3"),
        "u-",
        "*",
    ]


def test_all_operators():
    """Test all four binary operators."""
    assert parse("1 + 2 - 3 * 4 / 5") == [
        Decimal("1"),
        Decimal("2"),
        "+",
        Decimal("3"),
        Decimal("4"),
        "*",
        Decimal("5"),
        "/",
        "-",
    ]


def test_empty_parentheses_raises_error():
    """Empty parentheses raise ParsingError."""
    with pytest.raises(ParsingError, match="empty parentheses"):
        parse("()")


def test_unmatched_opening_paren():
    """Unmatched ( raises ParsingError."""
    with pytest.raises(ParsingError, match="unmatched opening parenthesis"):
        parse("(2 + 3")


def test_unmatched_closing_paren():
    """Unmatched ) raises ParsingError."""
    with pytest.raises(ParsingError, match="unmatched closing parenthesis"):
        parse("2 + 3)")


def test_expression_with_spaces():
    """Spaces do not affect parsing."""
    assert parse("  2   +   3  ") == [Decimal("2"), Decimal("3"), "+"]


def test_decimal_numbers():
    """Decimal numbers are parsed correctly."""
    result = parse("0.1 + 0.2")
    assert result == [Decimal("0.1"), Decimal("0.2"), "+"]
