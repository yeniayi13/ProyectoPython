from src.product.application.schemas.product_schema import Product, ProductCreate
from src.product.application.repositories.product_repository import ProductRepository
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from src.common.utils.result import Result

class CreateProductService(ApplicationService[ProductCreate, Result[Product]]):

    def __init__(
        self,
        product_repository: ProductRepository
    ):
        super().__init__()
        self.product_repository = product_repository

    async def execute(self, data: ProductCreate) -> Result[Product]:
        try:
            product = await self.product_repository.create(data)
            return Result.success(product)
        except Exception as e:
            print(f"Error al crear el producto: {e}")
            return Result.failure(Error('Internal Error', f'Error getting products: {str(e)}', 500))