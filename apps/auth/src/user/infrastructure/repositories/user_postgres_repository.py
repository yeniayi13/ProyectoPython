from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, exc
from src.user.infrastructure.schemas.user_schermas import User_in_create
from src.common.infrastructure.config.database.postgres_base_repository import Base_repository
from src.user.application.repositories.user_repository import User_repository
from src.user.infrastructure.models.user import User
from src.auth.application.commands.sign_up.types.sign_up_dto import Sign_up_dto
from datetime import datetime

class User_postgres_repository(Base_repository,User_repository,):

    async  def create_user(self, user):
        current_time = datetime.now() 
        user_in_create = User_in_create( id = user.id, first_name = user.first_name,
            last_name = user.last_name, c_i = user.c_i, username = user.username,
            email = user.email, password = user.password,role = user.role.value,
            created_at = current_time, updated_at = current_time)

        try:
            new_user = User(**user_in_create.model_dump( exclude_none=True ) )
            
            if not new_user:
                return {'code':500, 'msg':'A problem was found while creating a new user'}
            
            self.session.add(instance=new_user)
            self.session.commit()
            self.session.refresh(instance=new_user)
            
            return new_user
        except IntegrityError as e:
           # if 'duplicate key value violates unique constraint' in str(e):
            if 'duplicate key value violates unique constraint "users_c_i_key"' in str(e):
                return {'code':409,'msg':'C.I already associated to a User'}
            if 'duplicate key value violates unique constraint "users_username_key"' in str(e):
                return {'code':409,'msg':'username already associated to a user'}
            raise e  # Re-raise the error if it's something else

    async def user_exists(self,email:str) -> bool:
        #print('user exist: ',email, username)
        user =  await self.find_user(identification=email)
        return bool(user)

    
    async def find_user(self, identification:str):
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





#{
#    'code': 'gkpj', 
#    'statement': 'INSERT INTO users (id, first_name, last_name, c_i, username, email, password, role, created_at, updated_at) VALUES (%(id)s, %(first_name)s, %(last_name)s, %(c_i)s, %(username)s, %(email)s, %(password)s, %(role)s, %(created_at)s, %(updated_at)s)', 
#    'params': {
#        'id': '4a382f8f-2489-4261-9cc9-6a442d2165d8', 'first_name': 'string', 'last_name': 'string', 'c_i': 'E-19426496', 'username': 'alfonso', 'email': 'alon@eple.com', 'password': '$2b$12$992hZWtijnM5pnPSIK0cjeA.eHuTEUDr8vXE4iqsBv9Ee1gqhnCCu', 'role': 'CLIENT', 'created_at': datetime.datetime(2024, 12, 14, 8, 5, 16, 676314), 'updated_at': datetime.datetime(2024, 12, 14, 8, 5, 16, 676314)
#        }, 
#    'orig': UniqueViolation('duplicate key value violates unique constraint "users_c_i_key"\nDETAIL:  Key (c_i)=(E-19426496) already exists.\n'), 
#    'ismulti': False, 
#    'hide_parameters': False, 
#    'detail': [], 
#    'connection_invalidated': False
#}