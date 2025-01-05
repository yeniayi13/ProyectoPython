from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.cart.infrastructure.repositories.cart_postgres_repository import Cart_postgres_repository
from src.common.infrastructure.config.database.database import get_db
from src.common.utils import result
from src.orders.application.services.commands.create_order.create_order_service import Create_order_service
from src.orders.infrastructure.repositories.orders_postgres_repository import Order_postgrs_repository

order_routes = APIRouter(
    prefix='/orders',
)

@order_routes.post('/create',tags=['order'])
async def create_order(client_id,response:Response, session: Session = Depends(get_db)):
    service = Create_order_service(
        cart_repository=Cart_postgres_repository(session),
        order_repository=Order_postgrs_repository(session),
    )
    result = await service.execute(client_id)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()


@order_routes.post('/cancel',tags=['order'])
async def cancel_order(msg:str):
    print(msg)
    return msg

'''@order_routes.put('',tags=['order'])
def approve_order(order_id:str):
    print(msg)
    return msg
'''

@order_routes.get('',tags=['order'])
async def get_all(msg:str):
    print(msg)
    return msg

    