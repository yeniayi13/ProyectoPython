from pydantic import BaseModel
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
        
    async def find_product(self, id:str):
        try:
            product =  self.session.query(Product).filter(Product.id == id ).first()
            return product
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
        
    async def product_exists(self,id:str) -> bool:
        product =  await self.find_product(id=id)
        return bool(product)
    
    async def modify_product(self, id:str, product_in_modify: BaseModel):
        try:
            product = await self.find_product(id)
            attributes =[] 
            if not product:
                return Result.failure(Error('ProductNotFound','The client does not exist in the system',404))
            
            
            for key,value in product_in_modify.model_dump(exclude_none=True).items():
                 setattr(product,key,value)
                 if (key != 'updated_at'):
                    attributes.append(key)        
            
            self.session.commit()
            
            
            return Result.success(product)
        
        except IntegrityError as e:
                return Result.failure(Error('IntegrityError','Info was provided does not match the requirements to be saved',409))
            
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))
            


