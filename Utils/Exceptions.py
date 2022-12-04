import typing

class MyCustomException(Exception):
    def __init__(self, message: str = "Error while processing consumer record"):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)