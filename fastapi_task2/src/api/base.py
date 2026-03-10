from fastapi import APIRouter, status

router = APIRouter(prefix="/base", tags=["Base"])


@router.get("/hello_world", status_code=status.HTTP_200_OK)
async def get_hello_world() -> dict:
    return {"text": "Hello, World!"}