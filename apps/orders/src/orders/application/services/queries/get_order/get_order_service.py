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
        

    
    async def execute(self,order_id:str)-> Result :
        if not (await self.order_repository.order_exists(order_id)):
            return Result.failure(Error('OrderNotExist','The order you are trying to cancel does not exist in the system',409))
        
        result = await self.order_repository.get_order(order_id)

       #print(result.result())
        

        #if result.is_error():
        #    return result

        #result = result.result()
        ##print(result[0].first_name)
        #order={
        #    'client': f'{result[0].first_name} {result[0].last_name}',
        #    'total':result[0].total_amount,
        #    'status':result[0].status,
        #    'items':[{
        #        'name':'',
        #        'quantity':0
        #    }]
        #}
        #products = [{
        #    'name':res.name,
        #    'quantity':res.quantity 
        #    } 
        #      for res in result]
#
        #order['items']=products
    
       # print(order)
        print(result.result())
        print(result)

        return result