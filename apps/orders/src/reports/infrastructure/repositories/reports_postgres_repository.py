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
            total_sales = self.session.query(
                func.sum(Order.total_amount).label("total_sales")
            ).filter(Order.status == "COMPLETED").scalar()

            if total_sales:
                return Result.success(total_sales)    
            return Result.success(0.0)
        except Exception as e:
            print('get_total_sales e:', e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))

    
    async def get_sales_by_product(self, product_id:str):
        try:
            sales = self.session.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(OrderItem.quantity).label("total_quantity_sold"),
                func.sum(OrderItem.quantity * Product.price).label("total_sales_amount")
            ).join(OrderItem, Product.id == OrderItem.product_id) \
             .join(Order, Order.id == OrderItem.order_id) \
             .filter(Product.id == product_id, Order.status == "COMPLETED") \
             .group_by(Product.id, Product.name).first()

            if sales:
                return Result.success({
                    "product_id": sales.product_id,
                    "product_name": sales.product_name,
                    "total_quantity_sold": sales.total_quantity_sold,
                    "total_sales_amount": sales.total_sales_amount
                })
            else:
                return Result.success({"message": "No sales data available for this product."})
                
                
        except Exception as e:
            print('get_sales_by product e:', e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))
        
    
    
    async def get_total_revenue(self):
        try:
            total_profit = self.session.query(
                func.sum((Product.price - Product.cost) * OrderItem.quantity).label("total_profit")
            ).select_from(Product) \
                .join(OrderItem, Product.id == OrderItem.product_id) \
                .join(Order, Order.id == OrderItem.order_id) \
                .filter(Order.status == "COMPLETED") \
                .scalar()

            if total_profit:
                return Result.success(total_profit)
            return Result.success(0.0)
            
        except Exception as e:
            print('get_total_revenue e:',e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))
    
   
    async def get_revenue_by_product(self, product_id:str):
        '''It does not work, hidden in swagger schema'''
        try :

            profit = self.session.query(
                 func.sum(Product.price * OrderItem.quantity).label("total_revenue")
            ).select_from(Product) \
             .join(OrderItem, Product.id == OrderItem.product_id) \
             .join(Order, Order.id == OrderItem.order_id) \
             .filter(Order.status == "COMPLETED") \
             .filter(Product.id == product_id) \
             .scalar()

            if profit:
                return Result( {
                "product_id": profit.product_id,
                "product_name": profit.product_name,
                "profit": profit.profit
                })
            else:
                return Result.success({"message": "No profit data available for this product."})
           
        except Exception as e:
           print('get_revenue_by_product e:',e)
           return Result.failure(Error('InternalServerError','Unexpected DB error',500))

    
    async def get_top_sold_products(self,limit=10):
        try:
            top_products = self.session.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                func.sum(OrderItem.quantity).label("total_quantity_sold")
            ).join(OrderItem, Product.id == OrderItem.product_id) \
             .join(Order, Order.id == OrderItem.order_id) \
             .filter(Order.status == "COMPLETED") \
             .group_by(Product.id, Product.name) \
             .order_by(func.sum(OrderItem.quantity).desc()) \
             .limit(limit).all()

            top_products = [
                {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "total_quantity_sold": product.total_quantity_sold
                }
                for product in top_products
            ]
            return Result.success(top_products)
                        
        except Exception as e:
            print('get_top_sold_products e:',e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))



    
    
    async def get_top_buyers(self, limit=10):
        try:
            top_customers = self.session.query(
                Client.id.label("client_id"),
                Client.first_name.label("first_name"),
                Client.last_name.label("last_name"),
                func.sum(Order.total_amount).label("total_spent")
                ).join(Order, Client.id == Order.client_id) \
                 .filter(Order.status == "COMPLETED") \
                 .group_by(Client.id, Client.first_name, Client.last_name) \
                 .order_by(func.sum(Order.total_amount).desc()) \
                 .limit(limit).all()

            top_customers = [
                {
                    "client_id": customer.client_id,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "total_spent": customer.total_spent
                }
                for customer in top_customers
            ]
            return Result.success(top_customers)
            
        except Exception as e:
            print('get_top_sold_products e:',e)
            return Result.failure(Error('InternalServerError','Unexpected DB error',500))