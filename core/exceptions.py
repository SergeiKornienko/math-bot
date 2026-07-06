"""Exception hierarchy for the math bot."""


class MathBotError(Exception):
    """Base exception. All bot errors inherit from this."""

    pass


class TokenizerError(MathBotError):
    """Raised when a string cannot be tokenized (unknown symbol)."""

    pass


class ParsingError(MathBotError):
    """Raised when token sequence has invalid syntax (unmatched parenthesis, wrong order)."""

    pass


class EvaluationError(MathBotError):
    """Raised when a valid expression cannot be evaluated (division by zero, overflow)."""

    pass
