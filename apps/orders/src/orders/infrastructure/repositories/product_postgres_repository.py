from src.common.infrastructure.config.database.postgres_base_repository import Base_repository
from src.orders.application.schemas.product_schemas import Product_in_create
from src.common.utils.result import Result
from src.common.utils.errors import Error
from src.orders.application.repositories.product_repository import Product_repository
from src.orders.infrastructure.models.product import Product
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

class Product_postgres_repository(Base_repository,Product_repository):
    
    async def create_product(self,product:Product_in_create):
        try:
            new_product = Product(**product.model_dump( exclude_none=True ) )
            
            if not new_product:
                return Result.failure(Error('ProductNotCreated','A problem was found while creating a new Product',500))
            
            self.session.add(instance=new_product)
            self.session.commit()
            self.session.refresh(instance=new_product)

            return Result.success(new_product)
        except IntegrityError as e:
            print('IntegrityError:',e)
        print('e: ',e)
        return Result.failure(Error('UnknownError','There is no clue about this error',500))  
        
    async def find_product(self, identification:str):
        try:
            product =  self.session.query(Product).filter(Product.id == identification ).first()
            
            print('product',product)

            return product
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
        
    async def product_exists(self,id:str) -> bool:
        product =  await self.find_product(identification=id)
        return bool(product)


