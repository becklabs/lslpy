class ContractViolation(Exception):
    def __init__(self, message="Contract violation"):
        self.message = message
        super().__init__(self.message)

class GenerateError(Exception):
    def __init__(self, contract) -> None:
        self.message = f"Cannot generate {contract}"
        super().__init__(self.message)