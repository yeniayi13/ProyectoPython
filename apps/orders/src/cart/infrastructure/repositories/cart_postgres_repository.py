from src.cart.application.repositories.cart_repository import Cart_repository
from src.cart.application.services.commands.add_product.types.app_product_dto import Add_product_dto
from src.common.infrastructure.config.database.postgres_base_repository import Base_repository
from src.common.utils.errors import Error
from src.common.utils.result import Result
from src.orders.infrastructure.models.cart import Cart


class Cart_postgres_repository(Base_repository,Cart_repository):
    
    async def add_product_to_cart(self, product:Add_product_dto):
        try:
            cart=Cart(**product.model_dump(exclude_none=True))
            if not cart:
                return Result.failure(Error('ProductNotAddedToCart','A problem was found while adding the product to the cart',500))
            
            
            self.session.add(instance=cart)
            self.session.commit()
            self.session.refresh(instance=cart) 

            return Result.success(True)           

        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
        


    async def product_already_in_cart(self, id:str):
        try:
            product = self.session.query(Cart).filter(
                Cart.product_id==id
            ).first()

            return bool(product)
        except Exception as e:
            print(e)
            
    