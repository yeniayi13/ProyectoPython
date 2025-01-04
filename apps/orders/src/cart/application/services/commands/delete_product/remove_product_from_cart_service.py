from src.cart.application.repositories.cart_repository import Cart_repository
from src.cart.application.schemas.cart_schemas import Cart_in_delete
from src.cart.application.services.commands.delete_product.types.remove_product_from_cart_dto import Remove_product_from_cart_dto
from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.common.utils.errors import Error
from src.orders.application.repositories.product_repository import Product_repository


class Remove_product_from_cart_service(ApplicationService):


    def __init__(
            self, 
            cart_repository:Cart_repository,
            product_repo: Product_repository,
    ):
        super().__init__()
        self.cart_repository = cart_repository
        self.product_repo = product_repo


    
    async def execute(self,dto:Remove_product_from_cart_dto)-> Result :
        if  not ( await self.product_repo.product_exists(dto.product_id)):
            return Result.failure(Error('ProductNotExists','The product which is being tried to add to the cart does not exist in the system',404))
        
        if not (await self.cart_repository.product_already_in_cart(dto.product_id,dto.client_id)):
            return Result.failure(Error('ProductIsNotInTheCart','The product does not exist in the cart, you should add it first',409))
        
        product = Cart_in_delete(client_id=dto.client_id, product_id= dto.product_id)
        result:Result = await self.cart_repository.remove_product_from_cart(product)

        if(result.is_error()):
            return result
        
        return Result.success(f'Product {dto.product_id} removed succesfully from your cart')   