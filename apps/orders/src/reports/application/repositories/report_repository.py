from abc import ABC, abstractmethod


class ReportRepository(ABC):
    @abstractmethod
    def get_total_sales():
        pass

    @abstractmethod
    def get_sales_by_product(id:str):
        pass
    
    @abstractmethod
    def get_total_revenue():
        pass

    
    @abstractmethod
    def get_revenue_by_product(id:str):
        pass

    @abstractmethod
    def get_revenue_by_product(id:str):
        pass

    @abstractmethod
    def get_top_sold_products():

        pass
    
    @abstractmethod
    def get_top_buyers():
        pass
    