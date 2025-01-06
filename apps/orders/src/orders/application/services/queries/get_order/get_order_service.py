from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.common.utils.errors import Error
from src.orders.application.repositories.orders_repository import Order_repository



class Get_order_service(ApplicationService):


    def __init__(
            self, 
            order_repository:Order_repository
    ):
        super().__init__()
        self.order_repository = order_repository
        

    
    async def execute(self,order_id:str, client_id)-> Result :
        if not (await self.order_repository.order_exists(order_id)):
            return Result.failure(Error('OrderNotExist','The order you are trying to retrieve does not exist in the system',409))
        if (client_id !=None) and not (await self.order_repository.verify_order_belongs_to_user(order_id, client_id)):
            return Result.failure(Error('OrderNotBelongTothisUser','The order you are trying to retrieve does not belong to you',409))
        
        result = await self.order_repository.get_order(order_id)

        print(result.result())
        print(result)

        return result