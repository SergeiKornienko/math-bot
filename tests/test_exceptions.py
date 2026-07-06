"""Tests for the exception hierarchy."""

import pytest
from core.exceptions import (
    MathBotError,
    TokenizerError,
    ParsingError,
    EvaluationError,
)


def test_exceptions_hierarchy():
    """All exceptions must be subclasses of MathBotError."""
    assert issubclass(TokenizerError, MathBotError)
    assert issubclass(ParsingError, MathBotError)
    assert issubclass(EvaluationError, MathBotError)


def test_tokenizer_error():
    """TokenizerError is raised with a message."""
    with pytest.raises(TokenizerError, match="unknown symbol"):
        raise TokenizerError("unknown symbol: @")


def test_parsing_error():
    """ParsingError is raised with a message."""
    with pytest.raises(ParsingError, match="unmatched parenthesis"):
        raise ParsingError("unmatched parenthesis")


def test_evaluation_error():
    """EvaluationError is raised with a message."""
    with pytest.raises(EvaluationError, match="division by zero"):
        raise EvaluationError("division by zero")


def test_catch_all_by_base():
    """All errors can be caught via the base MathBotError."""
    for error_class in [TokenizerError, ParsingError, EvaluationError]:
        try:
            raise error_class("test")
        except MathBotError:
            pass
        else:
            pytest.fail(
                f"{error_class.__name__} not caught as MathBotError"
            )
