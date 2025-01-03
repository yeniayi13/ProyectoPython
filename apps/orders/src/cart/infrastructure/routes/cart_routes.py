from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from src.cart.application.services.commands.add_product.add_product_service import Add_product_service
from src.cart.application.services.commands.add_product.types.app_product_dto import Add_product_dto
from src.cart.infrastructure.repositories.cart_postgres_repository import Cart_postgres_repository
from src.cart.infrastructure.routes.entries.add_product_entry import Add_product_entry
from src.common.infrastructure.config.database.database import get_db
from src.orders.infrastructure.repositories.client_postgres_repository import Client_postgres_repository
from src.orders.infrastructure.repositories.product_postgres_repository import Product_postgres_repository

cart_routes = APIRouter(
    prefix='/cart',
)

@cart_routes.post('/add_product',tags=['cart'])
async def add_product(
    entry:Add_product_entry, 
    response:Response,
    session: Session = Depends(get_db)):
    
    dto = Add_product_dto(client_id=entry.client_id, product_id=entry.product_id, quantity=entry.quantity )
    service = Add_product_service(
        cart_repository=Cart_postgres_repository(session),
        product_repo= Product_postgres_repository(session),
        client_repo= Client_postgres_repository(session)
    )
    result = await service.execute(dto)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()



#@cart_routes.post('/add_one',tags=['cart'])
#async def add_one(id:str, session: Session = Depends(get_db)):
#    service = 
#    print(id)
#    return id


@cart_routes.post('/remove_one',tags=['cart'])
async def remove_one(msg:str, session: Session = Depends(get_db)):
    print(msg)
    return msg




@cart_routes.delete('delete',tags=['cart'])
async def delete_product(msg:str, session: Session = Depends(get_db)):
    print(msg)
    return msg
