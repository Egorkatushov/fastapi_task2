from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.post_repository import PostRepository
from ....infrastructure.sqlite.repositories.user_repository import UserRepository
from ....infrastructure.sqlite.repositories.category_repository import CategoryRepository
from ....infrastructure.sqlite.repositories.location_repository import LocationRepository
from ....schemas.post import PostCreate, Post
from ....core.exceptions.post_exceptions import (
    PostAuthorNotFoundException,
    PostCategoryNotFoundException,
    PostLocationNotFoundException,
    PostAlreadyExistsException  # ← ДОБАВЬТЕ ЭТОТ ИМПОРТ
)
from sqlalchemy.exc import IntegrityError  # ← ДОБАВЬТЕ ЭТОТ ИМПОРТ


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._user_repo = UserRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_data: PostCreate) -> Post:
        with self._database.session() as session:
            # ← ДОБАВЬТЕ ЭТУ ПРОВЕРКУ
            existing_post = self._repo.get(session, post_data.id)
            if existing_post:
                raise PostAlreadyExistsException(post_data.id)

            author = self._user_repo.get(session, post_data.author_id)
            if not author:
                raise PostAuthorNotFoundException(post_data.author_id)

            if post_data.category_id:
                category = self._category_repo.get(session, post_data.category_id)
                if not category:
                    raise PostCategoryNotFoundException(post_data.category_id)

            if post_data.location_id:
                location = self._location_repo.get(session, post_data.location_id)
                if not location:
                    raise PostLocationNotFoundException(post_data.location_id)

            try:
                post = self._repo.create(session, post_data)
                return Post.model_validate(post)
            except IntegrityError:
                session.rollback()
                raise PostAlreadyExistsException(post_data.id)