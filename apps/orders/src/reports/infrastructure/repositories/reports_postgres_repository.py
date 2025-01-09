from sqlalchemy import func
from src.common.infrastructure.config.database.postgres_base_repository import Base_repository
from src.common.utils.result import Result
from src.orders.infrastructure.models.order import Order
from src.orders.infrastructure.models import OrderItem
from src.orders.infrastructure.models.product import Product
from src.reports.application.repositories.report_repository import ReportRepository
from src.orders.infrastructure.models.client import Client
from src.common.utils.errors import Error

class ReportPostgresRepository(Base_repository,ReportRepository):



    async def get_total_sales(self):
        try:
            total_sales = self.session.query(func.sum(Order.total_amount)).scalar()
            if total_sales:
                return Result.success(total_sales)    
            return Result.success(0)
        except Exception as e:
            print('get_total_sales e:', e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))

    
    async def get_sales_by_product(self, product_id:str):
        try:
            sales = self.session.query(OrderItem.quantity * float(Product.price)). \
                filter(OrderItem.product_id == product_id). \
                join(Product).scalar()
            
            print(sales)
            return Result.success(sales)
        except Exception as e:
            print('get_sales_by product e:', e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))
        
    
    
    async def get_total_revenue(self):
        try:
            total_profit = self.session.query(
                sum((OrderItem.quantity * Product.price) - (OrderItem.quantity * Product.cost))
                ).scalar()
            
            print(total_profit)
            return Result.success(total_profit)
        except Exception as e:
            print('get_total_revenue e:',e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))
    
    
    async def get_revenue_by_product(self, product_id:str):
        try :
            total_profit = self.session.query(
                sum((OrderItem.quantity * Product.price) - (OrderItem.quantity * Product.cost))
                ).filter(OrderItem.product_id == product_id).join(Product).scalar()
            return Result.success(total_profit)
        except Exception as e:
            print('get_revenue_by_product e:',e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))

    
    async def get_top_sold_products(self,limit=10):
        try:
            result = self.session.query(
                Product, 
                func.sum(OrderItem.quantity).label('total_quantity')) \
                .join(OrderItem) \
                .group_by(Product.id) \
                .order_by(func.sum(OrderItem.quantity).desc()) \
                .limit(limit)
            return Result.success(result)
                        
        except Exception as e:
            print('get_top_sold_products e:',e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))



    
    
    def get_top_buyers(self, limit=10):
        try:
            result = self.session.query(
                Client, func.sum(Order.total_amount).label('total_spent')) \
                .join(Order) \
                .group_by(Client.id) \
                .order_by(func.sum(Order.total_amount).desc()) \
                .limit(limit)
            return Result.success(result)
        except Exception as e:
            print('get_top_sold_products e:',e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))
