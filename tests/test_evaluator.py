"""Tests for the postfix evaluator."""

from decimal import Decimal

import pytest

from core.evaluator import evaluate
from core.exceptions import EvaluationError
from core.parser import to_postfix
from core.tokenizer import tokenize


def calc(expr: str) -> Decimal:
    """Helper: tokenize -> parse -> evaluate."""
    return evaluate(to_postfix(tokenize(expr)))


def test_single_number():
    """A single number evaluates to itself."""
    assert calc("42") == Decimal("42")


def test_simple_addition():
    """2 + 3 = 5"""
    assert calc("2 + 3") == Decimal("5")


def test_subtraction():
    """5 - 3 = 2"""
    assert calc("5 - 3") == Decimal("2")


def test_multiplication():
    """4 * 7 = 28"""
    assert calc("4 * 7") == Decimal("28")


def test_division():
    """10 / 4 = 2.5"""
    assert calc("10 / 4") == Decimal("2.5")


def test_precedence():
    """2 + 3 * 4 = 14"""
    assert calc("2 + 3 * 4") == Decimal("14")


def test_parentheses():
    """(2 + 3) * 4 = 20"""
    assert calc("(2 + 3) * 4") == Decimal("20")


def test_unary_minus():
    """-5 + 3 = -2"""
    assert calc("-5 + 3") == Decimal("-2")


def test_unary_minus_in_parentheses():
    """(-5) = -5"""
    assert calc("(-5)") == Decimal("-5")


def test_unary_minus_with_multiplication():
    """2 * -3 = -6"""
    assert calc("2 * -3") == Decimal("-6")


def test_decimal_addition():
    """0.1 + 0.2 = 0.3 (exact with Decimal)"""
    assert calc("0.1 + 0.2") == Decimal("0.3")


def test_complex_expression():
    """(1 + 2) * (3 + 4) / 2 = 10.5"""
    assert calc("(1 + 2) * (3 + 4) / 2") == Decimal("10.5")


def test_division_by_zero():
    """Division by zero raises EvaluationError."""
    with pytest.raises(EvaluationError, match="division by zero"):
        calc("5 / 0")


def test_integer_division_by_zero():
    """Integer division by zero also raises."""
    with pytest.raises(EvaluationError, match="division by zero"):
        calc("0 / 0")
