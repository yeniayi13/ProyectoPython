
import uuid
from sqlalchemy import UUID
from src.cart.infrastructure.models.cart import Cart
from src.common.infrastructure.config.database.postgres_base_repository import Base_repository
from src.common.utils.errors import Error
from src.common.utils.result import Result
from src.orders.infrastructure.models.client import Client
from src.orders.infrastructure.models.order_items import OrderItem
from src.orders.application.repositories.orders_repository import Order_repository
from src.orders.application.schemas.order_schemas import Order_in_response, Product_in_order
from src.orders.infrastructure.models.order import Order
from sqlalchemy.exc import SQLAlchemyError

from src.orders.infrastructure.models.product import Product

class Order_postgrs_repository (Base_repository,Order_repository):

    async def create_order(self, client_id:str, products: list[Product_in_order])->Result[str]:
        total_amount = self.sum_product_prices(products)
        try:
                order_id=uuid.uuid4()
                order = Order( )
                order=Order(**
                    {
                    'id':order_id,
                    'client_id': client_id,
                    'total_amount':total_amount,
                    'status':'PENDING'
                })

                self.session.add(instance=order)

                order_items = [
                    OrderItem(
                        order_id=order_id,
                        product_id=product.id,
                        quantity=product.quantity
                )
                for product in products
                ]
                self.session.bulk_save_objects(order_items)    

                delete =self.session.query(Cart).filter(
                    Cart.client_id==client_id
                ).delete()    
                print(delete)

                self.session.commit()
                
                return Result.success(order_id)
        
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Transaction failed: {e}")
            return Result.failure(Error('FailedTransaction','Transaction was not completed',500))  
        except Exception as e:    
            self.session.rollback()
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
    
    async def sum_product_prices(self, products: list[Product_in_order]):
        sum = 0

        for product in products:
            sum += product.price*product.quantity
        return sum


    

    
    async def cancel_order(self,order_id):
        try:
            order = await self.find_order(order_id)
            if (order.status == 'COMPLETED'):
                return Result.failure(Error('OrderStatusIncorrect',f'This order is already completed, completed orders cannot be cancelled',409))
            if (order.status == 'CANCELLED'):
                return Result.failure(Error('OrderStatusIncorrect',f'This order is already cancelled',409))
            order.status = 'CANCELLED'
            self.session.commit()
            return Result.success(True)
        except Exception as e:
            print(e)    
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
    


    async def complete_order(self,order_id):
        try:
            order = await self.find_order(order_id)
            
            if (order.status == 'COMPLETED'):
                return Result.failure(Error('OrderStatusIncorrect',f'This order is already completed',409))
            if (order.status == 'CANCELLED'):
                return Result.failure(Error('OrderStatusIncorrect',f'This order is already cancelled, cancelled orders cannot be completed',409))
            order.status = 'COMPLETED'
            self.session.commit()
            return Result.success(True)
        except Exception as e:
            print(e)    
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
    
    
    async def find_order(self, order_id:str):
         
            order = self.session.query(Order).filter(
                Order.id==order_id
            ).first()
            return order
    
        
    async def order_exists(self, order_id:str):
        return bool(await self.find_order(order_id))
    
    async def get_order(self,order_id:str):
        try:
            result = self.session.query(
                Client.first_name, 
                Client.last_name, 
                Order.total_amount, 
                Order.status, 
                Product.name, 
                OrderItem.quantity
            ).filter(
                Order.id == OrderItem.order_id, 
                OrderItem.product_id == Product.id, 
                Client.id == Order.client_id, 
                Order.id == order_id  # The specific order you're interested in
            ).all()

            result =self.create_order(result)

            return Result.success(result)
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
        
    
    async def get_all_orders(self, client_id):
        try:
            result = self.session.query(
                Client.first_name, 
                Client.last_name, 
                Order.total_amount, 
                Order.status, 
                Product.name, 
                OrderItem.quantity
            ).filter(
                Order.id == OrderItem.order_id, 
                OrderItem.product_id == Product.id, 
                Client.id == Order.client_id, 
                Order.client_id == client_id  # The specific order you're interested in
            ).all()
            
            return Result.success(result)
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  





    def create_order(self, _order):
        order={
            'client': f'{_order[0].first_name} {_order[0].last_name}',
            'total':_order[0].total_amount,
            'status':_order[0].status,
            'items':[{
                'name':'',
                'quantity':0
            }]
        }
        products = [{
            'name':res.name,
            'quantity':res.quantity 
            } 
              for res in _order]

        order['items']=products
        
        return order

    async def find_orders(self, client_id:str):
        try:
            orders = self.session.query(Order).filter(
                Order.client_id==client_id
            ).all()
            
            orders=[
                Order_in_response(
                    id= order.id,
                    status= order.status,
                    total=order.total_amount ,
                    date = order.created_at          
                    )
                for order in orders
            ] 

            return Result.success(orders)
        except Exception as e:
            print('find_orders_postgres e:',e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  


    