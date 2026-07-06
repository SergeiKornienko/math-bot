"""Exception hierarchy for the math bot."""


class MathBotError(Exception):
    """Base exception. All bot errors inherit from this."""

    pass


class TokenizerError(MathBotError):
    """Raised when a string cannot be tokenized."""

    pass


class ParsingError(MathBotError):
    """Raised when token sequence has invalid syntax."""

    pass


class EvaluationError(MathBotError):
    """Raised when expression cannot be evaluated."""

    pass
