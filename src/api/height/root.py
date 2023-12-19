from fastapi import APIRouter

height_router = APIRouter()


@height_router.get("/")
async def root():
    return {"message": "Hello Height"}
