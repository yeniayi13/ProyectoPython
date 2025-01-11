import json
from src.common.application.application_services import ApplicationService
from src.common.application.ports.request_handler import Request_handler
from src.common.infrastructure.config.config import get_settings
from src.common.utils.result import Result
from src.common.utils.errors import Error
from src.orders.application.repositories.orders_repository import Order_repository

settings =get_settings()

class Cancel_order_service(ApplicationService):


    def __init__(
            self, 
            order_repository:Order_repository,
            request_handler: Request_handler

    ):
        super().__init__()
        self.order_repository = order_repository
        self.request_handler = request_handler
        

    
    async def execute(self,order_id:str, client_id:str)-> Result :
        if not (await self.order_repository.order_exists(order_id)):
            return Result.failure(Error('OrderNotExist','The order you are trying to cancel does not exist in the system',409))
        if (client_id !=None) and not (await self.order_repository.verify_order_belongs_to_user(order_id, client_id)):
            print('!= none')
            return Result.failure(Error('OrderNotBelongTothisUser','The order you are trying to cancel does not belong to you',409))
        
        result = await self.order_repository.cancel_order(order_id)
        

        if result.is_error():
            print(result.get_error_message()) 
            return result

        products=result.result()['items']
        products= [
            {
                "id":product['id'], 
                "quantity":product['quantity']
            } 
            for product in products]
        print('products to be sent:',products)

        products_restablished = await self.request_handler.replenish_cancelled_products(route=settings.ORDER_CANCELLED_ROUTE, products=products )
        

        return Result.success(f'The order {result.result()} has been cancelled')