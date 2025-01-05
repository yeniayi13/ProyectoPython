from src.cart.application.repositories.cart_repository import Cart_repository
from src.cart.application.schemas.cart_schemas import Cart_in_modify
from src.cart.application.services.commands.add_product.types.app_product_dto import Add_product_dto
from src.cart.application.services.commands.modify_quantity.types.modify_quantity_dto import Modify_cart_quantity_dto
from src.common.application.application_services import ApplicationService
from src.common.utils.result import Result
from src.common.utils.errors import Error
from src.orders.application.repositories.product_repository import Product_repository


class Modify_cart_quantity_service(ApplicationService):


    def __init__(
            self, 
            cart_repository:Cart_repository,
            product_repo: Product_repository,
    ):
        super().__init__()
        self.cart_repository = cart_repository
        self.product_repo = product_repo


    
    async def execute(self,dto:Modify_cart_quantity_dto)-> Result :
        if  not ( await self.product_repo.product_exists(dto.product_id)):
            return Result.failure(Error('ProductNotExists','The product which is being tried to add to the cart does not exist in the system',404))
        
        if not (await self.cart_repository.product_already_in_cart(dto.product_id,dto.client_id)):
            return Result.failure(Error('ProductIsNotInTheCart','The product does not exist in the cart, you should add it first',409))

        cart = Cart_in_modify(client_id=dto.client_id,product_id=dto.product_id, add= dto.add)
        result:Result = await self.cart_repository.modify_quantity_in_cart(cart)

        if (result.is_error()):
            return result
        
        if dto.add:
            print('add')
            return Result.success(f'You added one of the product {dto.product_id} to your cart')
        else:
            print('remove')
            return Result.success(f'You remove one of the product {dto.product_id} from your cart')   
        