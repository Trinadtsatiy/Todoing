class MissingEnvVariableError(Exception):
    def __init__(self, var_name: str, *args: object) -> None:
        message = f"Переменная {var_name} не задана"
        super().__init__(message, *args)
