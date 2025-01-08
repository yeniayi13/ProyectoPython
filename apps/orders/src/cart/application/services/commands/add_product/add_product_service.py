from src.cart.application.repositories.cart_repository import Cart_repository
from src.cart.application.services.commands.add_product.types.app_product_dto import Add_product_dto
from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.common.utils.errors import Error
from uuid import uuid4
from datetime import datetime


from src.orders.application.repositories.client_repository import Client_repository
from src.orders.application.repositories.product_repository import Product_repository


class Add_product_service(ApplicationService):


    def __init__(
            self, 
            cart_repository:Cart_repository,
            product_repo: Product_repository,
            client_repo: Client_repository
    ):
        super().__init__()
        self.cart_repository = cart_repository
        self.product_repo = product_repo
        self.client_repo = client_repo


    
    async def execute(self,dto: Add_product_dto)-> Result :
        if  not ( await self.product_repo.product_exists(dto.product_id)):
            return Result.failure(Error('ProductNotExists','The product which is being tried to add to the cart does not exist in the system',404))
        
        if (await self.cart_repository.product_already_in_cart(dto.product_id, dto.client_id)):
            return Result.failure(Error('ProductAlreadyInTheCart','The product already exists in the cart',409))

        
        result:Result = await self.cart_repository.add_product_to_cart(dto)

        if (result.is_error()):
            return result
        
        return Result.success(f'Product {dto.product_id} Added succesfully to your cart')   