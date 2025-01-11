from datetime import datetime
from uuid import uuid4
from src.product.application.schemas.product_schema import Product
from src.common.infrastructure.config.config import get_settings
from src.common.utils.optional import Optional
from src.product.infrastructure.routes.inventory_routes import get_inventory_repository
import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from fastapi import status
from main import app

settings = get_settings()
JWT_TEST = settings.JWT_TEST

# FIXTURE PARA EL CLIENTE DE PRUEBAS CON OVERRIDE
@pytest.fixture
def client_with_override():
    # Crear cliente de prueba
    with TestClient(app) as client:
        yield client

    # LIMPIAR OVERRIDES DESPUÉS DEL TEST
    app.dependency_overrides.clear()

# TEST LISTAR CANTIDAD DE INVENTARIO DE UN PRODUCTO (CASO EXITOSO)
@pytest.mark.asyncio
async def test_list_quantity_of_product_inventory_success(client_with_override):
    # Mock del repositorio
    mock_inventory_repository = AsyncMock()
    mock_inventory_repository.get_by_id.return_value = Optional.of(Product(
        id=str(uuid4()),
        code="P001",
        name="Product 1",
        description="Descripción del producto 1",
        cost=100.0,
        margin=0.2,
        price=125.0,
        quantity=100,
    ))
    
    # Sobrescribir la dependencia
    app.dependency_overrides[get_inventory_repository] = lambda: mock_inventory_repository

    # Realizar la solicitud
    product_id = str(uuid4())
    response = client_with_override.get(
        f"/inventories/{product_id}",
        headers={"Authorization": f"Bearer {JWT_TEST}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Product 1"
    assert response.json()["quantity"] == 100

# TEST LISTAR CANTIDAD DE INVENTARIO DE UN PRODUCTO (CASO FALLIDO)
@pytest.mark.asyncio
async def test_list_quantity_of_product_inventory_failure(client_with_override):
    # Mock del repositorio
    mock_inventory_repository = AsyncMock()
    mock_inventory_repository.get_by_id.side_effect = Exception("Database error")

    # Sobrescribir la dependencia
    app.dependency_overrides[get_inventory_repository] = lambda: mock_inventory_repository

    # Realizar la solicitud
    product_id = str(uuid4())
    response = client_with_override.get(
        f"/inventories/{product_id}",
        headers={"Authorization": f"Bearer {JWT_TEST}"},
    )

    # Verificar la respuesta
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "No se pudo obtener el producto"}

# TEST ACTUALIZAR CANTIDAD EN INVENTARIO DE UN PRODUCTO (CASO EXITOSO)
@pytest.mark.asyncio
async def test_update_quantity_of_product_success(client_with_override):
    # Mock del repositorio
    mock_inventory_repository = AsyncMock()
    mock_inventory_repository.update.return_value = Product(
        id=str(uuid4()),
        code="P001",
        name="Product 1",
        description="Descripción del producto 1",
        cost=100.0,
        margin=0.2,
        price=125.0,
        quantity=100,
    )

  

    # Sobrescribir la dependencia
    app.dependency_overrides[get_inventory_repository] = lambda: mock_inventory_repository

    # Realizar la solicitud
    product_id = str(uuid4())
    data = {"quantity": 100}
    response = client_with_override.put(
        f"/inventories/{product_id}",
        json=data,
        headers={"Authorization": f"Bearer {JWT_TEST}"},
    )

    # Verificar la respuesta
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Product 1"
    assert response.json()["quantity"] == 100

# # TEST ACTUALIZAR CANTIDAD EN INVENTARIO DE UN PRODUCTO (CASO FALLIDO)
@pytest.mark.asyncio
async def test_update_quantity_of_product_failure(client_with_override):
    # Mock del repositorio
    mock_inventory_repository = AsyncMock()
    mock_inventory_repository.update.side_effect = Exception("Database error")

    # Sobrescribir la dependencia
    app.dependency_overrides[get_inventory_repository] = lambda: mock_inventory_repository

    # Realizar la solicitud
    product_id = str(uuid4())
    data = {"quantity": 100}
    response = client_with_override.put(
        f"/inventories/{product_id}",
        json=data,
        headers={"Authorization": f"Bearer {JWT_TEST}"},
    )

    # Verificar la respuesta
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "No se pudo actualizar el producto"}