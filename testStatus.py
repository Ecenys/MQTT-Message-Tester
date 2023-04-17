class TestStatus(BaseException):
    def __init__(self, status):
        # Se valida que el estado sea uno de los valores permitidos
        if status not in ["waiting", "processing", "failed", "completed"]:
            raise ValueError("El estado no es válido")
        self.status = status

    def __str__(self):
        return f"Error: TestStatus -> Estado: {self.status}"

# Definición de la excepción FailedTest
class FailedTest(Exception):
    def __init__(self):
        pass

# Definición de la excepción CompletedTest
class CompletedTest(Exception):
    def __init__(self):
        pass