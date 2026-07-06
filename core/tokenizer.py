"""Tokenizer: splits a math expression string into tokens."""

from decimal import Decimal
from typing import List, Union

from core.exceptions import TokenizerError

Token = Union[Decimal, str]
"""A token is a number (Decimal) or an operator/parenthesis (str)."""

OPERATORS = {"+", "-", "*", "/", "(", ")"}


def tokenize(expression: str) -> List[Token]:
    """Convert a string expression into a list of tokens.

    Numbers are parsed as Decimal.
    Operators and parentheses are kept as single-character strings.
    Spaces are ignored.
    Unary minus is detected at start or after operator/parenthesis.
    """
    tokens: List[Token] = []
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char in OPERATORS:
            if char == "-" and _is_unary(tokens):
                tokens.append("-")
            else:
                tokens.append(char)
            i += 1
            continue

        if char.isdigit() or char == ".":
            start = i
            has_dot = char == "."
            i += 1
            while (
                i < n
                and (expression[i].isdigit() or expression[i] == ".")
            ):
                if expression[i] == ".":
                    if has_dot:
                        raise TokenizerError(
                            "invalid number: multiple dots"
                        )
                    has_dot = True
                i += 1
            num_str = expression[start:i]
            if num_str.startswith("."):
                num_str = "0" + num_str
            tokens.append(Decimal(num_str))
            continue

        raise TokenizerError(f"unknown symbol: {char!r}")

    return tokens


def _is_unary(tokens: List[Token]) -> bool:
    """Return True if the next '-' should be treated as unary."""
    if not tokens:
        return True
    last = tokens[-1]
    return last in {"+", "-", "*", "/", "("}
