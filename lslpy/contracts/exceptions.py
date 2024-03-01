class ContractViolation(Exception):
    def __init__(self, message="Contract violation"):
        self.message = message
        super().__init__(self.message)

class LowFuel(Exception):
    def __init__(self, message="Ran out of fuel during generate") -> None:
        self.message = message
        super().__init__(message)