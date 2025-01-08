from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from apps.product.src.product.infrastructure.routes.product_routes import get_product_repository
from src.common.domain.roles import Roles
from src.common.infrastructure.adapters.pika_event_handler import Pika_event_handler
from src.common.infrastructure.config.event_handler.event_handler_connection import get_channel
from src.common.infrastructure.dependencies.token_role_validator import require_roles
from src.product.application.schemas.product_schema import ProductQuantityUpdate, ProductUpdate
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

# • POST/inventories/{product_id}: Agrega productos al inventario
