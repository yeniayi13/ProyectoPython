from src.common.application.ports.event_handler import Event_handler
from src.product.application.schemas.product_schema import Product, ProductUpdate
from src.product.application.repositories.product_repository import ProductRepository
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from src.common.utils.result import Result

class UpdateProductService(ApplicationService[ProductUpdate, Result[Product]]):

    def __init__(
        self,
        product_repository: ProductRepository,
        event_handler:Event_handler
    ):
        super().__init__()
        self.product_repository = product_repository
        self.event_handler = event_handler

    async def execute(self, data: ProductUpdate) -> Result[Product]:
        try:
            _product =  await self.product_repository.get_by_id(data.id)
            
            if not _product.value:
                return Result.failure(Error('ProductNotExist', f'Product with ID {data} does not exist in the system', 409))
            
            product = await self.product_repository.update(data)
            
            event = {
            'id':str(product.id),
            'name':product.name ,
            'price':product.price,
            'quantity':product.quantity,
            'cost':product.cost
            }
            
            
            self.event_handler.publish(event,'products.product_updated','products')   

            return Result.success(product)
        except Exception as e:
            return Result.failure(Error('Internal Error', f'Error updatting product with ID {data}', 500))