from fastapi import APIRouter
from functions.test import get_building_height
height_router = APIRouter()


@height_router.get("/")
async def root():
    return {"message": "Hello Height"}

@height_router.get("/test")
async def test():
    height = get_building_height(33.5774038, 130.2582227)
    return {"target_height": height}