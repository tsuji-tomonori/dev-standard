from fastapi import APIRouter

from . import functions

router = APIRouter()

@router.get('/items/{item_id}')
async def get_item(item_id: str):
    item = functions.load_item(item_id)
    return functions.present_item(item)
