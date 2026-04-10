from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from typing import List

from ..schemas.category import Category, CategoryCreate, CategoryUpdate
from ..domain.category.use_cases.get_category import GetCategoryUseCase
from ..domain.category.use_cases.get_categories import GetCategoriesUseCase
from ..domain.category.use_cases.create_category import CreateCategoryUseCase
from ..domain.category.use_cases.update_category import UpdateCategoryUseCase
from ..domain.category.use_cases.delete_category import DeleteCategoryUseCase
from ..core.exceptions.category_exceptions import (
    CategoryNotFoundByIdException,
    CategoryAlreadyExistsException,
    CategoryNameAlreadyExistsException,
    CategoryTitleEmptyException,
    CategoryDescriptionEmptyException,
    CategorySlugEmptyException
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[Category], status_code=status.HTTP_200_OK)
async def get_categories(use_case: GetCategoriesUseCase = Depends()) -> List[Category]:
    """
    Получить список всех категорий
    """
    return await use_case.execute()


@router.get("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def get_category(
        category_id: int,
        use_case: GetCategoryUseCase = Depends()
) -> Category:
    """
    Получить категорию по ID
    """
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
        category_data: CategoryCreate,
        use_case: CreateCategoryUseCase = Depends()
) -> Category:
    """
    Создать новую категорию

    - **id**: уникальный идентификатор категории
    - **title**: название категории (не может быть пустым)
    - **description**: описание категории (не может быть пустым)
    - **slug**: уникальный идентификатор для URL (не может быть пустым)
    - **is_published**: опубликована ли категория
    - **created_at**: дата создания
    """
    try:
        return await use_case.execute(category_data=category_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except CategoryAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )
    except CategoryNameAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )
    except CategoryTitleEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.get_detail()
        )
    except CategoryDescriptionEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.get_detail()
        )
    except CategorySlugEmptyException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.get_detail()
        )


@router.put("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def update_category(
        category_id: int,
        category_data: CategoryUpdate,
        use_case: UpdateCategoryUseCase = Depends()
) -> Category:
    """
    Обновить категорию по ID
    """
    try:
        return await use_case.execute(
            category_id=category_id,
            category_data=category_data
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except CategoryNameAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
        category_id: int,
        use_case: DeleteCategoryUseCase = Depends()
) -> dict:
    """
    Удалить категорию по ID
    """
    try:
        return await use_case.execute(category_id=category_id)
    except CategoryNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )