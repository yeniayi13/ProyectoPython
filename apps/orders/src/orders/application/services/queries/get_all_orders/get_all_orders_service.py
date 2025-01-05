from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.common.utils.errors import Error
from src.orders.application.repositories.orders_repository import Order_repository



class Get_all_orders_service(ApplicationService):


    def __init__(
            self, 
            order_repository:Order_repository
    ):
        super().__init__()
        self.order_repository = order_repository
        

    
    async def execute(self,client_id:str)-> Result :
        #if not (await self.order_repository.order_exists(order_id)):
        #    return Result.failure(Error('OrderNotExist','The order you are trying to cancel does not exist in the system',409))
        
        result = await self.order_repository.find_orders(client_id)
        if result.is_error():
            return result
        return result