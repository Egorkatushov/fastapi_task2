from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.post_repository import PostRepository
from ....schemas.post import PostUpdate, Post


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, post_data: PostUpdate) -> Post:
        """Обновить пост"""
        try:
            with self._database.session() as session:
                # Проверяем существование поста
                post = self._repo.get(session, post_id)
                if not post:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пост с ID {post_id} не найден"
                    )

                # Обновляем пост
                update_data = post_data.model_dump(exclude_unset=True)
                updated_post = self._repo.update(session, post, **update_data)

                return Post.model_validate(updated_post)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении поста: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )