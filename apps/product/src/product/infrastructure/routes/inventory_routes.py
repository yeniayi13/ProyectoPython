from typing import Dict, List
from fastapi import APIRouter, Body, Depends, Response, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.product.application.services.replenish_products_service import Replenish_products_service
from src.product.infrastructure.routes.product_routes import get_product_repository
from src.common.domain.roles import Roles
from src.common.infrastructure.adapters.pika_event_handler import Pika_event_handler
from src.common.infrastructure.config.event_handler.event_handler_connection import get_channel
from src.common.infrastructure.dependencies.token_role_validator import require_roles
from src.product.application.schemas.product_schema import ProductQuantityUpdate, ProductUpdate, Replenish_products_entry
from src.product.application.repositories.product_repository import ProductRepository
from src.product.infrastructure.repositories.product_alchemy_repository import ProductAlchemyRepository
from src.product.application.services.get_product_by_id import GetProductByIdService
from src.product.application.services.update_product import UpdateProductService
from src.common.infrastructure.config.database.database import get_db

router = APIRouter(prefix="/inventories", tags=["Inventories"])

def get_inventory_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductAlchemyRepository(db)

@router.get("/{product_id}")
async def list_quantity_of_product_inventory(
    product_id: str, 
    product_repository: ProductRepository = Depends(get_inventory_repository),
    _ = Depends(require_roles([Roles.MANAGER]))
):
    service = GetProductByIdService(product_repository)
    try:
        product_id = UUID(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de producto inválido"
        )
    result = await service.execute(data=product_id)
    if result.is_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo obtener el producto"
        )
    elif result.get_data() is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    else:
        print('SE ESTÁ EJECUTANDO ESTOOOOO!!!!')
        print('SE ESTÁ EJECUTANDO ESTOOOOO!!!!')
        print('SE ESTÁ EJECUTANDO ESTOOOOO!!!!')
        print('SE ESTÁ EJECUTANDO ESTOOOOO!!!!')
        print(result.get_data())
        print(result.get_data().id)
        print(result.get_data().quantity)
        print(result.get_data().name)
        return {
            "product_id": result.get_data().id,
            "quantity": result.get_data().quantity,
            "name": result.get_data().name,
        }
    
#• PUT /inventories/{product_id}: Actualiza la cantidad en inventario de un producto.
@router.put("/{product_id}")
async def update_quantity_of_product(
    product_id: str, 
    data: ProductQuantityUpdate,
    product_repository: ProductRepository = Depends(get_product_repository),
    _ = Depends(require_roles([Roles.MANAGER])),
    channel = Depends(get_channel)
):
    try:
        product_id = UUID(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de producto inválido"
        )
    event_handler =Pika_event_handler(channel)
    service = UpdateProductService(product_repository, event_handler)
    result = await service.execute(data=ProductUpdate(id=product_id, quantity=data.quantity))
    if result.is_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo actualizar el producto"
        )
    else:
        return result.get_data()
    
@router.put("/verify_product_quantity/{product_id}/{quantity}",include_in_schema=False)
async def verify_product_quantitiy(
    product_id: str,
    quantity:int,
    response:Response,
    product_repository: ProductRepository = Depends(get_inventory_repository),
    channel = Depends(get_channel),
    
):
    try:
        product_id = UUID(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de producto inválido"
        )
    
    quantity_validator_service = GetProductByIdService(product_repository)
    result = await quantity_validator_service.execute(data=product_id)
    print(result)
    if result.is_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo obtener el producto"
        )
    elif result.get_data() is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    print(result.get_data())
    if result.get_data().quantity < quantity:
        response.status_code = 409
        return {
            'code':409,
            'msg': 'The amount of products available is inferior to what is needed' 
            } 
    
    new_quantity = result.get_data().quantity - quantity
    event_handler =Pika_event_handler(channel)
    discount_service = UpdateProductService(product_repository, event_handler)
    result = await discount_service.execute(data=ProductUpdate(id=product_id, quantity=new_quantity))
    if result.is_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo actualizar el producto"
        )
    
    response.status_code = 200
    return {
            'code': 200,
            'msg': 'Product can be added to the cart' 
            }



@router.put("/replenish_products/",include_in_schema=False)
async def replenish_products_cancelled_order(
    body:list[dict],
    response:Response,
    product_repository: ProductRepository = Depends(get_inventory_repository),
    channel = Depends(get_channel)
):

    event_handler =Pika_event_handler(channel)
    service = Replenish_products_service(product_repository, event_handler)
    body = [
        ProductUpdate( id= product['id'], quantity= product['quantity'])
        for product in body
    ]
    
    result = await service.execute(data=body)
    if result.is_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudieron actualizar la cantidad de los productos"
        )
    
    
    response.status_code = 200
    return {'msg':'Inventory updated'}
    
    
   


# • POST/inventories/{product_id}: Agrega productos al inventario

#@router.put("/replenish_products")
#async def test2(
#    body: List[Replenish_products_entry]):
#    print(body)
#    return{5}