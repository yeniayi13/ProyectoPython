from fastapi import APIRouter

auth_router = APIRouter(
    prefix='/auth',
    tags=["auth"])

@auth_router.post('/sign_up')
def sign_up():
    return {'route':'sign_up'}


@auth_router.post('/log_in')
def log_in():
    return {'route': 'log_in'}