from fastapi import APIRouter

order_routes = APIRouter(
    prefix='/orders',
)

@order_routes.post('/create',tags=['order'])
def create_order(msg:str):
    print(msg)
    return msg


@order_routes.post('/cancel',tags=['order'])
def cancel_order(msg:str):
    print(msg)
    return msg


@order_routes.get('',tags=['order'])
def get_all(msg:str):
    print(msg)
    return msg

@order_routes.put('',tags=['order'])
def update_order(msg:str):
    print(msg)
    return msg
    