from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.orders.application.repositories.client_repository import Client_repository
from src.orders.application.repositories.product_repository import Product_repository
from src.reports.application.repositories.report_repository import ReportRepository


class GetTopProductsService(ApplicationService):


    def __init__(
            self, 
            report_repository:ReportRepository
    ):
        super().__init__()
        self.report_repository = report_repository
        

    
    async def execute(self)-> Result :

        result:Result = await self.report_repository.get_top_sold_products()

        if (result.is_error()):
            return result
        
        return Result.success(result.result())  