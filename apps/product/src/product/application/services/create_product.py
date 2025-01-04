from src.common.application.ports.event_handler import Event_handler
from src.product.application.schemas.product_schema import Product, ProductCreate
from src.product.application.repositories.product_repository import ProductRepository
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from src.common.utils.result import Result

class CreateProductService(ApplicationService[ProductCreate, Result[Product]]):

    def __init__(
        self,
        product_repository: ProductRepository,
        event_handler: Event_handler
    ):
        super().__init__()
        self.product_repository = product_repository
        self.event_handler = event_handler

    async def execute(self, data: ProductCreate) -> Result[Product]:
        try:
            product = await self.product_repository.create(data)

            event = {
            'id':str(product.id),
            'name':product.name ,
            'price':product.price,
            'quantity':product.quantity
            }
            event_result = self.event_handler.publish(event,'products.product_created','products')
            print()
            if event_result :
                print('Product event published succesfully!')
            else:
                print('Product event was not published, something happen!')
            return Result.success(product)
        except Exception as e:
            print(f"Error al crear el producto: {e}")
            return Result.failure(Error('Internal Error', f'Error getting products: {str(e)}', 500))