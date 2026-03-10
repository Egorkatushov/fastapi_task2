from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.post_repository import PostRepository
from ....schemas.post import Post
from typing import List, Optional


class GetPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(
        self,
        category_id: Optional[int] = None,
        location_id: Optional[int] = None,
        author_id: Optional[int] = None
    ) -> List[Post]:
        """Получить список всех постов с возможностью фильтрации"""
        try:
            with self._database.session() as session:
                posts = self._repo.get_all(
                    session,
                    category_id=category_id,
                    location_id=location_id,
                    author_id=author_id
                )
                return [Post.model_validate(post) for post in posts]

        except Exception as e:
            print(f"Ошибка при получении списка постов: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )