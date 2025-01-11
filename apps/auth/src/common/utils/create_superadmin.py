
from src.auth.application.commands.create_superadmin.create_superadmin_service import Create_superadmin_service
from src.auth.application.commands.create_superadmin.types.create_superadmin_dto import Create_superadmin_dto
from src.user.infrastructure.repositories.user_postgres_repository import User_postgres_repository
from src.user.application.models.user import Roles
from src.common.application.application_services import ApplicationService
from src.common.infrastructure.adapters.bcrypt_hash_helper import Bcrypt_hash_helper
from src.common.infrastructure.adapters.pika_event_handler import Pika_event_handler
from src.common.infrastructure.config.database.database import get_db
from src.common.infrastructure.config.event_handler.event_handler_connection import get_channel
from pika.adapters.blocking_connection import BlockingChannel
from sqlalchemy.orm import Session

from src.common.utils.result import Result

session: Session=next(get_db())
channel:BlockingChannel = next(get_channel()) 

async def create_superadmin_at_start():
    role = Roles.SUPERADMIN
    dto = Create_superadmin_dto(first_name='Alfonso', last_name='Blanco', c_i='V-28027626', 
                username='superadmin',email='superadmin@example.com', password='stringst', role=role)
    service:ApplicationService = Create_superadmin_service( 
        user_repository = User_postgres_repository(session),
        hash_helper=Bcrypt_hash_helper(),
        event_handler=Pika_event_handler(channel=channel))
    result:Result = await service.execute(dto)
    
    if result.is_error():
        if result.error.name == 'ExistingEmail':
            print('Superadmin is already created')
        else:
            print('Error:',result.get_error_message())
    else:   
        print('Superadmin_created succesfully')