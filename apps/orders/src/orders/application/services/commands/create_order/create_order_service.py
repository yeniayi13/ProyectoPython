from src.cart.application.repositories.cart_repository import Cart_repository
from src.cart.application.schemas.cart_schemas import Cart_in_response
from src.cart.application.services.commands.add_product.types.app_product_dto import Add_product_dto
from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.common.utils.errors import Error



from src.orders.application.repositories.client_repository import Client_repository
from src.orders.application.repositories.orders_repository import Order_repository
from src.orders.application.repositories.product_repository import Product_repository
from src.orders.application.schemas.order_schemas import Product_in_order


class Create_order_service(ApplicationService):


    def __init__(
            self, 
            cart_repository:Cart_repository,
            order_repository:Order_repository
    ):
        super().__init__()
        self.cart_repository = cart_repository
        self.order_repository = order_repository
        

    
    async def execute(self,client_id:str)-> Result :
        result = await self.cart_repository.get_cart(client_id)
        if not result.result():
            return Result.failure(Error('CartEmpty','There are no products in the cart with which an order can be created,',409))
        
        cart=[]
        for item in result.result():
            item_response =Product_in_order(
                id=item[2],
                quantity=item[1],
                price=item[3],
            )
            cart.append(item_response)
        
        
        result = await self.order_repository.create_order(client_id, cart)
        if result.is_error():
            return result

        return Result.success(f'A new order has been created with this id: {result.result()} ')