class ContractViolation(Exception):
    def __init__(self, message="Contract violation"):
        self.message = message
        super().__init__(self.message)
