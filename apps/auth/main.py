from src.common.infrastructure.config.database.init_db import create_tables
from src.auth.infrastructure.routes.auth_routes import auth_router
from src.user.infrastructure.routes.user_routes import user_routes
from fastapi import FastAPI
from contextlib import asynccontextmanager


async def lifespan(app:FastAPI):
    print('initializing Auht DB at start')
    try:
        create_tables()
        yield
    except Exception as e:
        print(e)           
    

app = FastAPI(
    title='AuthService',
    description='This service is in charge of authenticating users of the platform',
    version='1.0',
    #on_startup='',
    #on_shutdown='',
    #middleware='',
    lifespan= lifespan,
)







app.include_router(auth_router)
app.include_router(user_routes)

@app.get("/health",tags=["health"])
def healthcheck():
    return {'state': 'Running'}
