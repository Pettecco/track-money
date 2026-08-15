class DomainException(Exception):
    """Base class for all domain-level business rule violations."""

    def __init__(self, message: str):
        """Initialize the exception with a descriptive message."""
        super().__init__(message)
        self.message = message

    def __str__(self):
        """Return the exception message as its string representation."""
        return self.message

    @staticmethod
    def validate(condition: bool, message: str):
        """Raise a DomainException if the condition is not met."""
        if not condition:
            raise DomainException(message)
