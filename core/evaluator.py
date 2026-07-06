"""Evaluator: computes the result of a postfix (RPN) expression."""

from decimal import Decimal, DivisionByZero, InvalidOperation
from typing import List

from core.exceptions import EvaluationError

Token = Decimal | str


def evaluate(postfix: List[Token]) -> Decimal:
    """Evaluate a postfix expression and return the result.

    Supported operators: +, -, *, /, u- (unary minus).
    All arithmetic uses Decimal for exact decimal representation.
    """
    stack: List[Decimal] = []

    for token in postfix:
        if isinstance(token, Decimal):
            stack.append(token)

        elif token == "u-":
            if not stack:
                raise EvaluationError(
                    "missing operand for unary minus"
                )
            stack.append(-stack.pop())

        elif token in {"+", "-", "*", "/"}:
            if len(stack) < 2:
                raise EvaluationError(
                    f"missing operand for '{token}'"
                )
            b = stack.pop()
            a = stack.pop()
            try:
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                elif token == "/":
                    stack.append(a / b)
            except (DivisionByZero, InvalidOperation):
                raise EvaluationError("division by zero")

        else:
            raise EvaluationError(
                f"unknown operator: {token!r}"
            )

    if len(stack) != 1:
        raise EvaluationError(
            f"invalid expression: {len(stack)} values left on stack"
        )

    return stack[0]
