from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.user_repository import UserRepository


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> dict:
        with self._database.session() as session:
            deleted = self._repo.delete(session, user_id)  # Передаем ID, не объект
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id {user_id} not found"
                )
            return {"message": f"User {user_id} deleted successfully"}