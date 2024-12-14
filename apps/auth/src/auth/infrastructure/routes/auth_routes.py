from src.auth.application.commands.create_manager.types.create_manager_dto import Create_manager_dto
from src.auth.application.commands.create_manager.create_manager_service import Create_manager_service
from src.auth.infrastructure.routes.entries.create_manager_dto import Create_manager_entry
from src.auth.application.commands.sign_up.types.sign_up_dto import Sign_up_dto
from src.auth.application.commands.sign_up.sign_up_service import Sign_up_service
from src.auth.application.commands.log_in.log_in_service import Log_in_service
from src.auth.application.commands.log_in.types.log_in_dto import Log_in_dto
from src.auth.infrastructure.routes.entries.sign_up_dto import Sign_up_dto as sign_up_entry
from src.auth.infrastructure.routes.entries.log_in_dto import Log_in_dto as log_in_entry
from src.user.application.models.user import Roles
from src.user.infrastructure.repositories.user_postgres_repository import User_postgres_repository
from src.common.application.application_services import ApplicationService
from src.common.infrastructure.adapters.JWT_auth_handler import JWT_auth_handler
from src.common.infrastructure.adapters.bcrypt_hash_helper import Bcrypt_hash_helper
from src.common.infrastructure.config.database.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

auth_router = APIRouter(
    prefix='/auth',
    tags=["auth"])

@auth_router.post('/sign_up', status_code=201)
async def sign_up(entry:sign_up_entry, session: Session = Depends(get_db) ):
    role = Roles.CLIENT
    dto = Sign_up_dto(first_name=entry.first_name, last_name=entry.last_name, c_i=entry.c_i, 
                username=entry.username,email=entry.email, password=entry.password, role=role)
    service:ApplicationService = Sign_up_service( user_repository = User_postgres_repository(session),hash_helper=Bcrypt_hash_helper())
    response = await service.execute(dto)
    return response


@auth_router.post('/log_in',status_code=200)
async def log_in(entry:log_in_entry, session: Session = Depends(get_db) ):
    dto =Log_in_dto(user= entry.user, password = entry.password)
    service = Log_in_service(
        user_repository = User_postgres_repository(session), 
        hash_helper=Bcrypt_hash_helper(),
        auth_handler=JWT_auth_handler())
    result = await service.execute(dto)
    return {'token':result}


@auth_router.post('/create_manager', status_code=201)
async def create_manager(entry:Create_manager_entry, session: Session = Depends(get_db)):
    role = Roles.MANAGER
    dto = Create_manager_dto(first_name=entry.first_name, last_name=entry.last_name, c_i=entry.c_i, 
                username=entry.username,email=entry.email, password=entry.password, role=role)
    service:ApplicationService = Create_manager_service( user_repository = User_postgres_repository(session),hash_helper=Bcrypt_hash_helper())
    response = await service.execute(dto)
    return response