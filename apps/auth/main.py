from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.common.infrastructure.config.database.init_db import create_tables

async def lifespan(app:FastAPI):
    print('initializing DB at start')
    try:
        create_tables()
        yield
    except Exception as e:
        print(e)           
    

app = FastAPI(
    title='AuthService',
    description='This service isin charfe of authenticated users of the platform',
    version='1.0',
    #on_startup='',
    #on_shutdown='',
    #middleware='',
    lifespan= lifespan
    
)

@app.get("/health")
def healthcheck():
    return {'state': 'Running'}