from uuid import UUID
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.domain.roles import Roles
from src.common.infrastructure.adapters.pika_event_handler import Pika_event_handler
from src.common.infrastructure.config.event_handler.event_handler_connection import get_channel
from src.common.infrastructure.dependencies.token_role_validator import require_roles
from src.common.infrastructure.config.database.database import get_db
from src.product.application.repositories.product_repository import ProductRepository
from src.product.application.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from src.product.application.services.create_product import CreateProductService
from src.product.application.services.delete_product import DeleteProductService
from src.product.application.services.get_all_products import GetAllProductsService
from src.product.application.services.get_product_by_id import GetProductByIdService
from src.product.application.services.update_product import UpdateProductService
from src.product.infrastructure.repositories.product_alchemy_repository import ProductAlchemyRepository

router = APIRouter(prefix="/products", tags=["Products"])

def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductAlchemyRepository(db)

@router.get("", response_model=list[ProductResponse])
async def list_products(
    product_repository: ProductRepository = Depends(get_product_repository)
):
    service = GetAllProductsService(product_repository)
    result = await service.execute()
    
    if result.is_error():
        print(result.get_error_message())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo obtener la lista de productos"
        )
    else: return result.get_data()

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    product_repository: ProductRepository = Depends(get_product_repository),
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
        return result.get_data()

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, 
    product_repository: ProductRepository = Depends(get_product_repository),
    _ = Depends(require_roles([Roles.MANAGER])),
    channel = Depends(get_channel)
):
    event_handler =Pika_event_handler(channel)
    service = CreateProductService(product_repository,event_handler)
    serviceResponse = await service.execute(data=product)
    if serviceResponse.is_success(): return serviceResponse.get_data()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No se pudo crear el producto"
        )

@router.put("", response_model=ProductResponse)
async def update_product(
    product: ProductUpdate,
    response:Response,
    product_repository: ProductRepository = Depends(get_product_repository),
    _ = Depends(require_roles([Roles.MANAGER])),
    channel = Depends(get_channel)
):
    event_handler =Pika_event_handler(channel)
    service = UpdateProductService(product_repository,event_handler)
    print(f'El producto a editar es: {product}')
    result = await service.execute(data=product)
    if 'does not exist in the system' in result.get_error_message():
        print('hello')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail='Product does not exist in the system'
        )
    if result.is_error():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="No se pudo actualizar el producto"
        )
    return result.get_data()

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str, 
    product_repository: ProductRepository = Depends(get_product_repository),
    _ = Depends(require_roles([Roles.MANAGER])),
    channel = Depends(get_channel)
): 
    event_handler =Pika_event_handler(channel)
    service = DeleteProductService(product_repository, event_handler)
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
            detail="No se pudo eliminar el producto"
        )

