from src.common.utils.result import Result
from src.user.application.schemas.user_schermas import User_in_create, User_in_modify, User_in_response
from src.common.infrastructure.config.database.postgres_base_repository import Base_repository
from src.user.application.repositories.user_repository import User_repository
from src.user.infrastructure.models.user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from src.common.utils.errors import Error


class User_postgres_repository(Base_repository,User_repository):

    async  def create_user(self, user:User_in_create) -> User_in_response:
        try:
            new_user = User(**user.model_dump( exclude_none=True ) )
            
            if not new_user:
                return Result.failure(Error('UserNotCreated','A problem was found while creating a new user',500))
            
            self.session.add(instance=new_user)
            self.session.commit()
            self.session.refresh(instance=new_user)

            return Result.success(new_user)
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint "users_c_i_key"' in str(e):
                return Result.failure(Error('CI_AlreadyInSystem','C.I already associated to a User',409))
            if 'duplicate key value violates unique constraint "users_username_key"' in str(e):
                return Result.failure(Error('UsernameAlreadyInSystem','Username already associated to a User',409))
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  

    async def user_exists(self,email:str) -> bool:
        user =  await self.find_user(identification=email)
        return bool(user)

    
    async def find_user(self, identification:str) -> User_in_response:
        try:
            user =  self.session.query(User).filter(
                or_(
                    User.username == identification,
                    User.email == identification,
                    User.id == identification 
                )).first()

            return user
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
        

    async def count_roles(self,role) -> int :
        try:
            users =  self.session.query(User).\
                filter(User.role == role,).all()
            return len(users)
        except Exception as e:
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
        


    async def create_manager(self, user)->Result[User_in_response]:
        try:
            #if (await self.count_roles('MANAGER') > 4 ):
            #    return {'code':409,'msg':'There are already the max amount of managers in the system'}
            new_user = User(**user.model_dump( exclude_none=True ) )
            if not new_user:
                return Result.failure(Error('UserNotCreated','A problem was found while creating a new manager',500))
            
            self.session.add(instance=new_user)
            self.session.commit()
            self.session.refresh(instance=new_user)
            
            return Result.success(new_user)                
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint "users_c_i_key"' in str(e):
                return Result.failure(Error('CI_AlreadyInSystem','C.I already associated to a User',409))
            if 'duplicate key value violates unique constraint "users_username_key"' in str(e):
                return Result.failure(Error('UsernameAlreadyInSystem','Username already associated to a User',409))
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))  
            

    async def create_superadmin(self, user:User_in_create)->Result[User_in_response]:
        try:
           # if (await self.count_roles('SUPERADMIN') > 1 ):
           #     return {'code':409,'msg':'There are already the max amount of SUPERADMINS in the system'}
            new_user = User(**user.model_dump( exclude_none=True ) )
            if not new_user:
                return Result.failure(Error('UserNotCreated','A problem was found while creating a new SUPERADMIN',500))
                
            self.session.add(instance=new_user)
            self.session.commit()
            self.session.refresh(instance=new_user)
            return Result.success(new_user)
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint "users_c_i_key"' in str(e):
                return Result.failure(Error('CI_AlreadyInSystem','C.I already associated to a User',409))
            if 'duplicate key value violates unique constraint "users_username_key"' in str(e):
                return Result.failure(Error('UsernameAlreadyInSystem','Username already associated to a User',409))
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))   
                
                             
    async def modify_client(self, id:str, user_in_modify: User_in_modify):
        try:
            user = await self.find_user(id)
            attributes =[] 
            if not user:
                return Result.failure(Error('UserNotFound','The user does not exist in the system',404))
            
            
            for key,value in user_in_modify.model_dump(exclude_none=True).items():
                 setattr(user,key,value)
                 if (key != 'updated_at'):
                    attributes.append(key)        
            
            self.session.commit()
            
            return Result.success(user)
            #return attributes
        
        except IntegrityError as e:
           # if 'duplicate key value violates unique constraint' in str(e):
            if 'duplicate key value violates unique constraint "users_c_i_key"' in str(e):
                return Result.failure(Error('CI_AlreadyInSystem','C.I already associated to a User',409))
            if 'duplicate key value violates unique constraint "users_username_key"' in str(e):
                return Result.failure(Error('UsernameAlreadyInSystem','Username already associated to a User',409))
            print(e)
            return Result.failure(Error('UnknownError','There is no clue about this error',500))
            


    async def find_managers(self):
        try:
            managers =  self.session.query(User).\
                    filter(User.role == 'MANAGER').all()
            return managers
        except Exception as e:
            raise e            
        
    async def is_manager(self,id:str) -> bool:
        try:
            user =  await self.find_user(identification=id)
            print(user.role)
            if user.role == 'MANAGER':
                return True
            return False
        except Exception as e:
             raise e