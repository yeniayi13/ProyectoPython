from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.orders.application.repositories.product_repository import Product_repository
from src.reports.application.repositories.report_repository import ReportRepository
from src.common.utils.errors import Error

class GetProductSalesService(ApplicationService):


    def __init__(
            self, 
            product_repository:Product_repository,
            report_repository:ReportRepository
    ):
        super().__init__()
        self.report_repository = report_repository
        self.product_repository = product_repository
        

    
    async def execute(self, product_id:str)-> Result :
        if not ( await self.product_repository.product_exists(product_id)):
            return Result.failure(Error('ProductNotExist','The order you are trying to retrieve does not exist in the system',404))
        
        result:Result = await self.report_repository.get_sales_by_product(product_id)

        if (result.is_error()):
            return result
        
        return Result.success(result.result())  