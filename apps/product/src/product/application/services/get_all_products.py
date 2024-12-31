from src.product.application.repositories.product_repository import ProductRepository
from src.product.domain.product import Product
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from src.common.utils.result import Result

class GetAllProductsService(ApplicationService[None, Result[Product]]):

    def __init__(
        self,
        product_repository: ProductRepository
    ):
        super().__init__()
        self.product_repository = product_repository

    async def execute(self) -> Result[list[Product]]:
        try:
            products = await self.product_repository.get_all()
            return Result.success(products)
        except Exception as e:
            return Result.failure(Error('Internal Error', f'Error getting products: {str(e)}', 500))


