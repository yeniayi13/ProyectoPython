from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from src.product.infrastructure.routes.product_routes import router as product_router
from src.product.infrastructure.routes.inventory_routes import router as inventory_router
from src.common.infrastructure.config.database.init_db import create_tables

app = FastAPI()

app.include_router(product_router)
app.include_router(inventory_router)

# Configura HTTPBearer como esquema de seguridad
security_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Product Service",
        version="1.0.0",
        description="This service is on charge of maanging products, and its inventory ",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.on_event("startup")
async def on_startup():
    try:
        await create_tables()
    except Exception as e:
        print(f"Error al crear tablas: {e}")