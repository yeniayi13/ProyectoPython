from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from src.cart.infrastructure.repositories.cart_postgres_repository import Cart_postgres_repository
from src.common.infrastructure.adapters.JWT_auth_handler import JWT_auth_handler
from src.common.infrastructure.adapters.httpx_request_handler import Httpx_request_handler
from src.common.infrastructure.config.database.database import get_db
from src.common.utils import result
from src.common.utils.verify_role import verify_roles
from src.orders.application.services.commands.cancel_order.cancel_order_service import Cancel_order_service
from src.orders.application.services.commands.complete_order.complete_order_service import Complete_order_service
from src.orders.application.services.commands.create_order.create_order_service import Create_order_service
from src.orders.application.services.queries.get_all_orders.get_all_orders_service import Get_all_orders_service
from src.orders.application.services.queries.get_order.get_order_service import Get_order_service
from src.orders.infrastructure.repositories.orders_postgres_repository import Order_postgrs_repository

order_routes = APIRouter(
    prefix='/orders',
)

auth = JWT_auth_handler()


@order_routes.post('/create',tags=['order'], status_code=200)
async def create_order(
    response:Response, 
    session: Session = Depends(get_db),
    info = Depends(auth.decode)
    ):

    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload = info.result()

    if not verify_roles(payload['role'],['CLIENT']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }

    client_id= payload['user_id']


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
async def cancel_order(
    order_id:str, 
    response:Response, 
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
    ):

    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    payload = info.result()

    if not verify_roles(payload['role'],['CLIENT', 'MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }


    service = Cancel_order_service(
        order_repository=Order_postgrs_repository(session),
        request_handler= Httpx_request_handler()
    )
    if payload['role'] == 'CLIENT':
        client_id= payload['user_id']
        result = await service.execute(order_id, client_id)
    if payload['role'] == 'MANAGER':
        result = await service.execute(order_id, None)

    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    
    return result.result()


@order_routes.put('/complete',tags=['order'], status_code=200)
async def complete_order(
    order_id:str, 
    response:Response, 
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
    ):

    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload = info.result()

    if not verify_roles(payload['role'],['MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }

    service = Complete_order_service(
        order_repository=Order_postgrs_repository(session),
    )
    if payload['role'] == 'CLIENT':
        client_id= payload['user_id']
        result = await service.execute(order_id, client_id)
    if payload['role'] == 'MANAGER':
        result = await service.execute(order_id, None)

    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    
    return result.result()


@order_routes.get('/all',tags=['order'])
async def get_all( 
    response:Response,
    client_id: Optional[str] = None, 
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
    ):

    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload = info.result()

    if not verify_roles(payload['role'],['CLIENT','MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    if payload['role'] == 'CLIENT':
        if(payload['user_id']!=client_id) and client_id != None:
            response.status_code = 409
            return {'msg': 'The orders you are trying to cancel does not belong to you' }
        client_id= payload['user_id']
         
    elif client_id== None:
        response.status_code = 400
        return {'msg': 'No clientID was sent'}

    print(client_id)


    service = Get_all_orders_service(
        order_repository=Order_postgrs_repository(session),
    )
    result = await service.execute(client_id)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()
    

@order_routes.get('/one',tags=['order'])
async def get_one(
    order_id:str, 
    response:Response, 
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
    ):


    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    payload = info.result()

    if not verify_roles(payload['role'],['MANAGER','CLIENT']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }

    service = Get_order_service(
        order_repository=Order_postgrs_repository(session),
    )

    if payload['role'] == 'CLIENT':
        client_id= payload['user_id']
        result = await service.execute(order_id, client_id)
    if payload['role'] == 'MANAGER':
        result = await service.execute(order_id, None)
        
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()










