from fastapi import APIRouter

cart_routes = APIRouter(
    prefix='/cart',
)

@cart_routes.post('/add_product',tags=['cart'])
def add_product(msg:str):
    print(msg)
    return msg


@cart_routes.post('/add_one',tags=['cart'])
def add_one(msg:str):
    print(msg)
    return msg





@cart_routes.get('delete',tags=['cart'])
def delete_product(msg:str):
    print(msg)
    return msg
