from src.cart.application.repositories.cart_repository import Cart_repository
from src.cart.application.schemas.cart_schemas import Cart_in_response
from src.cart.application.services.commands.add_product.types.app_product_dto import Add_product_dto
from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.common.utils.errors import Error
from uuid import uuid4
from datetime import datetime


from src.orders.application.repositories.client_repository import Client_repository
from src.orders.application.repositories.product_repository import Product_repository


class Get_cart_service(ApplicationService):


    def __init__(
            self, 
            cart_repository:Cart_repository
    ):
        super().__init__()
        self.cart_repository = cart_repository
        

    
    async def execute(self,id:str)-> Result :
        
        result:Result = await self.cart_repository.get_cart(id)

        if (result.is_error()):
            return result
        
        cart=[]

        for item in result.result():
            item_response =Cart_in_response(
                name=item[0],
                quantity=item[1]
            )
            cart.append(item_response)
        
        
        return Result.success(cart)   