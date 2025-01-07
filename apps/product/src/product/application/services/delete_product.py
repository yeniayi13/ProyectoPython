from uuid import UUID
from src.common.application.ports.event_handler import Event_handler
from src.product.application.schemas.product_schema import ProductCreate
from src.product.application.repositories.product_repository import ProductRepository
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from src.common.utils.result import Result

class DeleteProductService(ApplicationService[UUID, Result[None]]):

    def __init__(
        self,
        product_repository: ProductRepository,
        event_handler: Event_handler
    ):
        super().__init__()
        self.product_repository = product_repository
        self.event_handler = event_handler

    async def execute(self, data: UUID) -> Result[None]:
        try:
            await self.product_repository.delete(product_id=data)

            event = {
                'id':str(data),
            }
            
            self.event_handler.publish(event,'products.product_deleted','products')
            return Result.success(None)
        except Exception as e:
            return Result.failure(Error('Internal Error', f'Error deletting product with ID: {data}', 500))