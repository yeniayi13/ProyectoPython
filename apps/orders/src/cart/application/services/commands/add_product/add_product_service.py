from src.common.infrastructure.config.config import get_settings
from src.common.application.ports.request_handler import Request_handler
from src.cart.application.repositories.cart_repository import Cart_repository
from src.cart.application.services.commands.add_product.types.app_product_dto import Add_product_dto
from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.common.utils.errors import Error
from uuid import uuid4
from datetime import datetime

settings =get_settings()
from src.orders.application.repositories.client_repository import Client_repository
from src.orders.application.repositories.product_repository import Product_repository


class Add_product_service(ApplicationService):


    def __init__(
            self, 
            cart_repository:Cart_repository,
            product_repo: Product_repository,
            client_repo: Client_repository,
            request_handler: Request_handler
    ):
        super().__init__()
        self.cart_repository = cart_repository
        self.product_repo = product_repo
        self.client_repo = client_repo
        self.request_handler = request_handler


    
    

    async def execute(self,dto: Add_product_dto)-> Result :
        if  not ( await self.product_repo.product_exists(dto.product_id)):
            return Result.failure(Error('ProductNotExists','The product which is being tried to add to the cart does not exist in the system',404))
        
        if (await self.cart_repository.product_already_in_cart(dto.product_id, dto.client_id)):
            return Result.failure(Error('ProductAlreadyInTheCart','The product already exists in the cart',409))

        product_available = await self.request_handler.discount_product_quantity(route=settings.PRODUCT_CAN_BE_ADDED_ROUTE, product_id=dto.product_id, quantity=dto.quantity, add=True)

        if  product_available['code'] ==409:
            return Result.failure(Error('ProductNotAvailable','The quantity required to satisfy the request does not exist ',409))

        if  product_available['code'] ==500:
            return Result.failure(Error('ProductServiceInternalError',product_available['msg'],500))

        result:Result = await self.cart_repository.add_product_to_cart(dto)

        if (result.is_error()):
            return result
        
        return Result.success(f'Product {dto.product_id} Added succesfully to your cart')   