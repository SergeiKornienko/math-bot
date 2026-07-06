"""Parser: converts token list to Reverse Polish Notation (postfix).

Implements the Shunting-yard algorithm by Edsger Dijkstra.
"""

from decimal import Decimal
from typing import List, Union

from core.exceptions import ParsingError

Token = Union[Decimal, str]

PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "u-": 3,
}


def to_postfix(tokens: List[Token]) -> List[Token]:
    """Convert infix token list to postfix (RPN).

    Unary minus is detected by context and represented as 'u-'.
    """
    output: List[Token] = []
    operators: List[str] = []
    prev: Token | None = None

    for token in tokens:
        if isinstance(token, str) and token == "(":
            operators.append(token)

        elif isinstance(token, str) and token == ")":
            if isinstance(prev, str) and prev == "(":
                raise ParsingError("empty parentheses")
            _pop_until_left_paren(operators, output)

        elif isinstance(token, str) and token == "-":
            if _is_unary(prev):
                _pop_operators("u-", operators, output)
                operators.append("u-")
            else:
                _pop_operators("-", operators, output)
                operators.append("-")

        elif isinstance(token, str):
            _pop_operators(token, operators, output)
            operators.append(token)

        else:
            output.append(token)

        prev = token

    while operators:
        op = operators.pop()
        if op == "(":
            raise ParsingError("unmatched opening parenthesis")
        output.append(op)

    return output


def _is_unary(prev: Token | None) -> bool:
    """Return True if '-' at current position is unary."""
    if prev is None:
        return True
    if isinstance(prev, str) and prev in {"+", "-", "*", "/", "("}:
        return True
    return False


def _pop_operators(
    op: str,
    operators: List[str],
    output: List[Token],
) -> None:
    """Pop operators with higher or equal precedence."""
    op_prec = PRECEDENCE.get(op, 0)
    while operators and operators[-1] != "(":
        top_prec = PRECEDENCE.get(operators[-1], 0)
        if top_prec >= op_prec:
            output.append(operators.pop())
        else:
            break


def _pop_until_left_paren(
    operators: List[str],
    output: List[Token],
) -> None:
    """Pop operators until '(' is found.

    Raises ParsingError if no '(' is found.
    Empty parentheses are checked before calling this function.
    """
    while operators:
        op = operators.pop()
        if op == "(":
            return
        output.append(op)
    raise ParsingError("unmatched closing parenthesis")
