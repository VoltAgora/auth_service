from app.domain.models.user import User
from app.domain.ports.db_port import UserRepositoryPort

class AuthService:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    def login(self, email: str, password: str) -> User | None:
        user = self.user_repository.get_by_email(email)
        if not user:
            return None
        # Aquí luego se verifica la contraseña con bcrypt
        return user

    def register(self, user_data: User) -> User:
        return self.user_repository.save(user_data)
