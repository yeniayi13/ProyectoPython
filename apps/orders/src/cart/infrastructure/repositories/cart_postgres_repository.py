from src.cart.application.repositories.cart_repository import Cart_repository
from src.cart.application.schemas.cart_schemas import Cart_in_delete, Cart_in_modify
from src.cart.application.services.commands.add_product.types.app_product_dto import Add_product_dto
from src.common.infrastructure.config.database.postgres_base_repository import Base_repository
from src.common.utils.errors import Error
from src.common.utils.result import Result
from src.cart.infrastructure.models.cart import Cart
from sqlalchemy import and_

from src.orders.infrastructure.models.product import Product

class Cart_postgres_repository(Base_repository,Cart_repository):
    
    async def add_product_to_cart(self, product:Add_product_dto):
        try:
            cart=Cart(**product.model_dump(exclude_none=True))
            
            self.session.add(instance=cart)
            self.session.commit()
            self.session.refresh(instance=cart) 

            return Result.success(True)           

        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
        


    async def product_already_in_cart(self, product_id:str, client_id:str):
        try:
            product = self.session.query(Cart).filter(
                and_(
                Cart.client_id==client_id,
                Cart.product_id== product_id
            )
            ).first()

            return bool(product)
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  

    async def modify_quantity_in_cart(self, _cart:Cart_in_modify):
        try:
            cart:Cart = self.session.query(Cart).filter(
                and_(
                    Cart.client_id==_cart.client_id,
                    Cart.product_id== _cart.product_id
                )
            ).first()
            print(cart)
            if not cart:
                    return Result.failure(Error('ProductNotInTheCart','The product was not found in the cart',404))

            if(_cart.add):
                cart.quantity += 1
                self.session.commit()
                return Result.success(f'You added one of the product {_cart.product_id} to your cart')
            else:
                cart.quantity -= 1
                if not cart.quantity > 0:
                    return Result.failure(Error('OneProductInTheCart','You have just one element of this product, to be in the cart you need to have at least one',409))
                self.session.commit()
                return Result.success(f'You remove one of the product {_cart.product_id} from your cart')   
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  

    async def remove_product_from_cart(self, product:Cart_in_delete) -> Result:
        try:
            cart:Cart = self.session.query(Cart).filter(
                and_(
                    Cart.client_id==product.client_id,
                    Cart.product_id== product.product_id
                )
            ).first()

            self.session.delete(cart)
            self.session.commit()
            return Result.success(product.product_id)
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
        
    async def get_cart(self,client_id:str):
        try:
            carts = self.session.query(Product.name, Cart.quantity, Product.id, Product.price).\
                join(Cart, Product.id == Cart.product_id).\
                filter(Cart.client_id ==client_id ).\
                all()
            return Result.success(carts)
        except Exception as e:
            print(e)