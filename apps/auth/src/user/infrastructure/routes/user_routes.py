from fastapi import APIRouter

user_routes = APIRouter(
    prefix='/users',
    #tags=["user"]
)


@user_routes.delete('/client/:id', tags=['client'])
def delete_client(id):
    return {'route': f'delete client  {id}'}


@user_routes.put('/client/:id',tags=['client'])
def modify_client(id):
    return {'route':f'modify user {id}'}


@user_routes.get('/client/:id',tags=['client'])
def find_client(id):
    return {'route': f'find client {id}'}

@user_routes.post('/client/create', tags=['client'])
def create_client():
    return {'route': 'create_client'}








@user_routes.post('/manager/create', tags=['manager'])
def create_manager():
    return {'route': 'create_manager'}

@user_routes.delete('/manager/:id', tags=['manager'])
def delete_manager(id):
    return {'route': f'delete manager {id}'}

@user_routes.put('/manager/:id',tags=['manager'])
def modify_manager(id):
    return {'route':f'modify manager {id}'}


@user_routes.get('/manager/:id',tags=['manager'])
def find_manager(id):
    return {'route':f'find manager {id}'}

@user_routes.get('/manager/all',tags=['manager'])
def find_managers():
    return {'route':f'find manager all'}




@user_routes.post('/superadmin/create', tags=['superadmin'])
def create_superadmin():
    return {'route': 'create superadmin'}
