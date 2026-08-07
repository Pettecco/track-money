class DomainException(Exception):
    """Base class for all domain exceptions."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

    @staticmethod
    def validate(condition: bool, message: str):
        if not condition:
            raise DomainException(message)
