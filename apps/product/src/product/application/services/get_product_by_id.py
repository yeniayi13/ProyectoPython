from typing import Union
from uuid import UUID
from src.product.application.schemas.product_schema import Product
from src.product.application.repositories.product_repository import ProductRepository
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from src.common.utils.result import Result

class GetProductByIdService(ApplicationService[UUID, Result[Union[Product, None]]]):

    def __init__(
        self,
        product_repository: ProductRepository
    ):
        super().__init__()
        self.product_repository = product_repository

    async def execute(self, data: UUID) -> Result[Product]:
        try:
            product = await self.product_repository.get_by_id(id=data)
            if not product.has_value():
                return Result.success(None)
            #     return Result.failure(Error('Product not found', f'Product with id {data} not found', 404))
            return Result.success(product.get_value())
        except Exception as e:
            return Result.failure(Error('Internal Error', f'Error getting product with {data}: {str(e)}', 500))


