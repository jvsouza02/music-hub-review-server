class EmailAlreadyInUseException(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"The email {email} is already in use!")

class UserNotFoundException(Exception):
    def __init__(self, id: str):
        self.id = id
        super().__init__(f"User not found!")

class InvalidPasswordException(Exception):
    def __init__(self):
        super().__init__(f"Something went wrong! Incorrect email or password.")