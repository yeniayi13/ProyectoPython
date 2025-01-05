
import uuid
from sqlalchemy import UUID
from src.cart.infrastructure.models.cart import Cart
from src.common.infrastructure.config.database.postgres_base_repository import Base_repository
from src.common.utils.errors import Error
from src.common.utils.result import Result
from src.orders.infrastructure.models.order_items import OrderItem
from src.orders.application.repositories.orders_repository import Order_repository
from src.orders.application.schemas.order_schemas import Product_in_order
from src.orders.infrastructure.models.order import Order
from sqlalchemy.exc import SQLAlchemyError

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
    
    def sum_product_prices(self, products: list[Product_in_order]):
        sum = 0

        for product in products:
            sum += product.price*product.quantity
        return sum


    def find_order(id:str):
        pass
    

    def order_exists(email:str):
        pass

    

    def modify_order(id:str,user):
        pass
    
