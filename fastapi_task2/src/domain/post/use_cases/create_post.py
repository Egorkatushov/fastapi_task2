from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.post_repository import PostRepository
from ....schemas.post import PostCreate, Post


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_data: PostCreate) -> Post:
        """Создать новый пост"""
        try:
            with self._database.session() as session:
                # Здесь можно добавить проверки существования author_id, category_id, location_id
                new_post = self._repo.create(session, **post_data.model_dump())
                return Post.model_validate(new_post)

        except Exception as e:
            print(f"Ошибка при создании поста: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )