from fastapi import APIRouter

from functions.get_height import get_building_height
from functions.get_level import get_floor_level

height_router = APIRouter()


@height_router.get("/")
async def height(destName:str, destAddress:str, destLat:float, destLong:float):
    ceiling_height, level = get_building_height(destLat, destLong)
    if ceiling_height is None:
        ceiling_height = 3.0
    floor_level = get_floor_level(destAddress)
    print("floor_level", floor_level)
    if floor_level > 0:
        target_height = (floor_level - 1) * ceiling_height
    else:
        target_height = floor_level * ceiling_height
    print(target_height)
    return {"target_height": target_height, "floor_level": floor_level, "ceiling_height":ceiling_height, "building_level":level}

@height_router.get("/test")
async def test():
    height, level = get_building_height(33.5774038, 130.2582227)
    return {"target_height": height}