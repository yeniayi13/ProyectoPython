from http.client import HTTPException
from src.common.infrastructure.adapters.httpx_request_handler import Httpx_request_handler
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
import httpx
from src.cart.application.services.commands.add_product.add_product_service import Add_product_service
from src.cart.application.services.commands.add_product.types.app_product_dto import Add_product_dto
from src.cart.application.services.commands.delete_product.remove_product_from_cart_service import Remove_product_from_cart_service
from src.cart.application.services.commands.delete_product.types.remove_product_from_cart_dto import Remove_product_from_cart_dto
from src.cart.application.services.commands.modify_quantity.modify_quantity import Modify_cart_quantity_service
from src.cart.application.services.commands.modify_quantity.types.modify_quantity_dto import Modify_cart_quantity_dto
from src.cart.application.services.queries.get_cart_service import Get_cart_service
from src.cart.infrastructure.repositories.cart_postgres_repository import Cart_postgres_repository
from src.cart.infrastructure.routes.entries.add_product_entry import Add_product_entry
from src.common.infrastructure.adapters.JWT_auth_handler import JWT_auth_handler
from src.common.infrastructure.config.database.database import get_db
from src.common.utils.verify_role import verify_roles
from src.orders.infrastructure.repositories.client_postgres_repository import Client_postgres_repository
from src.orders.infrastructure.repositories.product_postgres_repository import Product_postgres_repository

cart_routes = APIRouter(
    prefix='/cart',
)

auth = JWT_auth_handler()

@cart_routes.post('/add_product',tags=['cart'])
async def add_product(
    entry:Add_product_entry, 
    response:Response,
    info = Depends(auth.decode),
    session: Session = Depends(get_db),
    ):

    if info.is_error():
        response.status_code = info.error.code
        return {
            'msg': info.get_error_message()
            }

    payload = info.result()
    if not verify_roles(payload['role'],['CLIENT']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    client_id= payload['user_id']

    dto = Add_product_dto(client_id=client_id, product_id=entry.product_id, quantity=entry.quantity )
    service = Add_product_service(
        cart_repository=Cart_postgres_repository(session),
        product_repo= Product_postgres_repository(session),
        client_repo= Client_postgres_repository(session),
        request_handler= Httpx_request_handler()
    )
    result = await service.execute(dto)
    if result.is_error():
        response.status_code = result.error.code
        return {
            'name': result.error.name,
            'msg': result.get_error_message() 
            } 
    return result.result()



@cart_routes.post('/add_one',tags=['cart'])
async def add_one(
    product_id:str, 
    response:Response, 
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
    ):
    
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    payload=info.result()

    if not verify_roles(payload   ['role'],['CLIENT']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }

    client_id= payload['user_id']

    dto= Modify_cart_quantity_dto(client_id=client_id, product_id= product_id, add=True)
    

    service=Modify_cart_quantity_service(
        cart_repository= Cart_postgres_repository(session),
        product_repo= Product_postgres_repository(session),
        request_handler= Httpx_request_handler()
    )
    result = await service.execute(dto) 
    if result.is_error():
        response.status_code = result.error.code
        
        return {
            'msg': result.get_error_message() 
            } 
    
    return result.result()



@cart_routes.post('/remove_one',tags=['cart'])
async def remove_one(
    product_id:str, 
    response:Response, 
    session: Session = Depends(get_db),
    info = Depends(auth.decode)
    ):

    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}
    
    payload=info.result()

    if not verify_roles(payload['role'],['CLIENT']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
        
    client_id= payload['user_id']

    dto= Modify_cart_quantity_dto(client_id=client_id, product_id= product_id, add=False)
    service=Modify_cart_quantity_service(
        cart_repository=Cart_postgres_repository(session),
        product_repo= Product_postgres_repository(session),
        request_handler= Httpx_request_handler()
    )
    result = await service.execute(dto)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()
    



@cart_routes.delete('delete',tags=['cart'])
async def delete_product(
    
    product_id:str, 
    response:Response, 
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
    ):

    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload=info.result()

    if not verify_roles(payload['role'],['CLIENT']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    client_id= payload['user_id']

    dto = Remove_product_from_cart_dto(client_id = client_id, product_id= product_id)
    service = Remove_product_from_cart_service(
        Cart_postgres_repository(session),
        product_repo= Product_postgres_repository(session)
        )
    result = await service.execute(dto)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()
    

@cart_routes.get('/',tags=['cart'])
async def get_cart(
    response:Response, 
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
    ):

    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload=info.result()

    if not verify_roles(payload['role'],['CLIENT']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    client_id= payload['user_id']

    service = Get_cart_service(Cart_postgres_repository(session))
    result = await service.execute(client_id)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()



# INVENTORY_URL = "http://localhost:8001/inventories/add_to_cart"
# @cart_routes.get("/test",tags=['cart'])
# async def test_httpx(order_item: str):
#     async with httpx.AsyncClient() as client:
#         try:
#             print(f"{INVENTORY_URL}/{order_item}")
#             print('hola')
#             # Realizar una solicitud al servicio de inventario
#             response = await client.get(f"{INVENTORY_URL}/{order_item}")
#             print(response)
#             inventory_item = response.json()
#             print(inventory_item)
            
#             # Aquí puedes añadir la lógica para procesar la orden
#             # Por ejemplo, reducir la cantidad del inventario
            
#             return {"message": "Order created", "inventory": inventory_item}
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(
#                 status_code=e.response.status_code,
#                 detail=e.response.json().get("detail", "Unknown error")
#             )