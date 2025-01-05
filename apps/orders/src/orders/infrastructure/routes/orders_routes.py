from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.cart.infrastructure.repositories.cart_postgres_repository import Cart_postgres_repository
from src.common.infrastructure.config.database.database import get_db
from src.common.utils import result
from src.orders.application.services.commands.cancel_order.cancel_order_service import Cancel_order_service
from src.orders.application.services.commands.complete_order.complete_order_service import Complete_order_service
from src.orders.application.services.commands.create_order.create_order_service import Create_order_service
from src.orders.application.services.queries.get_all_orders.get_all_orders_service import Get_all_orders_service
from src.orders.application.services.queries.get_order.get_order_service import Get_order_service
from src.orders.infrastructure.repositories.orders_postgres_repository import Order_postgrs_repository

order_routes = APIRouter(
    prefix='/orders',
)

@order_routes.post('/create',tags=['order'], status_code=200)
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


@order_routes.put('/cancel',tags=['order'], status_code=200)
async def cancel_order(order_id:str, response:Response, session: Session = Depends(get_db)):
    service = Cancel_order_service(
        order_repository=Order_postgrs_repository(session),
    )
    result = await service.execute(order_id)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()


@order_routes.put('/complete',tags=['order'], status_code=200)
async def complete_order(order_id:str, response:Response, session: Session = Depends(get_db)):
    service = Complete_order_service(
        order_repository=Order_postgrs_repository(session),
    )
    result = await service.execute(order_id)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()


@order_routes.get('/all',tags=['order'])
async def get_all(client_id:str, response:Response, session: Session = Depends(get_db)):
    service = Get_all_orders_service(
        order_repository=Order_postgrs_repository(session),
    )
    result = await service.execute(client_id)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()
    

@order_routes.get('/one',tags=['order'])
async def get_one(order_id:str, response:Response, session: Session = Depends(get_db)):
    service = Get_order_service(
        order_repository=Order_postgrs_repository(session),
    )
    result = await service.execute(order_id)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()


    














