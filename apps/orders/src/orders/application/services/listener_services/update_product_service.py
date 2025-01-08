from src.orders.application.schemas.product_schemas import Product_in_create, Product_in_update
from src.common.application.application_services import ApplicationService
from src.common.utils.errors import Error
from src.common.utils.result import Result
from src.orders.application.repositories.product_repository import Product_repository
#from src.orders.application.schemas.product_schemas import product_in_create
from src.orders.application.services.listener_services.listeners_dtos.create_product_dto import Create_product_dto




class Update_product_service(ApplicationService):
    def __init__(
            self,
            product_repository:Product_repository
            ):
        
        super().__init__()
        self.product_repository = product_repository

    async def execute(self,dto:Create_product_dto) -> Result[bool]:
        if not (await self.product_repository.product_exists(dto.id)):
            return Result.failure(Error(name='ProductNotExists', msg='This product does not exist in the system', code=409)) 
        
        
        product= Product_in_update(
            name= dto.name,
            price=dto.price,
            quantity=dto.quantity
        )
        
        
        new_product =  await self.product_repository.modify_product(dto.id, product)
        
        if new_product.is_error():
            return new_product
        
        new_product = new_product.result()
        return Result.success(True)