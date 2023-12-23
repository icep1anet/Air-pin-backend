from fastapi import APIRouter
from functions.test import get_building_height
height_router = APIRouter()


@height_router.get("/")
async def height(destName:str, destAddress:str, destLat:float, destLong:float):
    ceiling_height = get_building_height(destLat, destLong)
    if ceiling_height is None:
        ceiling_height = 3.0
    return {"target_height": ceiling_height}

@height_router.get("/test")
async def test():
    height = get_building_height(33.5774038, 130.2582227)
    return {"target_height": height}