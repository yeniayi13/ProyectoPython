from datetime import datetime
from uuid import uuid4
from src.common.infrastructure.config.config import get_settings
from src.common.infrastructure.dependencies.token_role_validator import require_roles
from src.product.infrastructure.routes.product_routes import get_product_repository
import pytest
from unittest.mock import AsyncMock, patch
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


# TEST LISTAR PRODUCTOS CASO EXITOSO
@pytest.mark.asyncio
async def test_list_products_success(client_with_override):
    # Mock del repositorio
    mock_product_repository = AsyncMock()
    mock_product_repository.get_all.return_value = [
        {
            "id": str(uuid4()),
            "code": "P001",
            "name": "Product 1",
            "description": "Descripción del producto 1",
            "cost": 100.0,
            "margin": 0.2,
            "price": 125.0,
            "quantity": 50,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        },
        {
            "id": str(uuid4()),
            "code": "P002",
            "name": "Product 2",
            "description": "Descripción del producto 2",
            "cost": 200.0,
            "margin": 0.25,
            "price": 266.67,
            "quantity": 30,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        },
    ]

    # Sobrescribir la dependencia
    app.dependency_overrides[get_product_repository] = lambda: mock_product_repository

    # Realizar la solicitud
    response = client_with_override.get("/products")

    # Verificar la respuesta
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Product 1"
    assert response.json()[0]["price"] == 125.0


# TEST LISTAR PRODUCTOS CASO FALLIDO
@pytest.mark.asyncio
async def test_list_products_failure(client_with_override):
    # Mock del repositorio que lanza una excepción
    mock_product_repository = AsyncMock()
    mock_product_repository.get_all.side_effect = Exception("Database error")

    # Sobrescribir la dependencia
    app.dependency_overrides[get_product_repository] = lambda: mock_product_repository

    # Realizar la solicitud
    response = client_with_override.get("/products")

    # Verificar la respuesta
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "No se pudo obtener la lista de productos"}

# TEST PARA LA CREACIÓN DE PRODUCTO
@pytest.mark.asyncio
async def test_create_product_success(client_with_override):
    # Mock del repositorio
    mock_product_repository = AsyncMock()
    mock_product_repository.create.return_value = {
        "id": str(uuid4()),
        "code": "P003",
        "name": "Product 3",
        "description": "Descripción del producto 3",
        "cost": 150.0,
        "margin": 0.3,
        "price": 195.0,
        "quantity": 40,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    # Sobrescribir la dependencia
    app.dependency_overrides[get_product_repository] = lambda: mock_product_repository

    # Datos para la creación del producto
    product_data = {
        "code": "P003",
        "name": "Product 3",
        "description": "Descripción del producto 3",
        "cost": 150.0,
        "margin": 0.3,
        "price": 195.0,
        "quantity": 40,
    }

    # Realizar la solicitud
    response = client_with_override.post(
        "/products",
        json=product_data,
        headers={"Authorization": f"Bearer {JWT_TEST}"}
    )

    # Verificar la respuesta
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Product 3"
    assert response.json()["price"] == 195.0


# TEST PARA LA ACTUALIZACIÓN DE PRODUCTO
@pytest.mark.asyncio
async def test_update_product_success(client_with_override):
    # Mock del repositorio
    mock_product_repository = AsyncMock()
    mock_product_repository.update.return_value = {
        "id": str(uuid4()),
        "code": "P001",
        "name": "Updated Product 1",
        "description": "Descripción actualizada",
        "cost": 110.0,
        "margin": 0.15,
        "price": 126.5,
        "quantity": 45,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    # Sobrescribir la dependencia
    app.dependency_overrides[get_product_repository] = lambda: mock_product_repository

    response = client_with_override.put(
        "/products",
        json={
            "id": str(uuid4()),
            "code": "P001",
            "name": "Updated Product 1",
            "description": "Descripción actualizada",
            "cost": 110.0,
            "margin": 0.15,
            "price": 126.5,
            "quantity": 45,
        },
        headers={"Authorization": f"Bearer {JWT_TEST}"}
    )

    # Verificar la respuesta
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product 1"
    assert response.json()["price"] == 126.5

# TEST PARA LA ELIMINACIÓN DE PRODUCTO
@pytest.mark.asyncio
async def test_delete_product_success(client_with_override):
    # Mock del repositorio
    mock_product_repository = AsyncMock()
    mock_product_repository.delete.return_value = None

    # Sobrescribir la dependencia
    app.dependency_overrides[get_product_repository] = lambda: mock_product_repository

    # Realizar la solicitud
    response = client_with_override.delete(f"/products/{uuid4()}", headers={"Authorization": f"Bearer {JWT_TEST}"})

    # Verificar la respuesta
    assert response.status_code == status.HTTP_204_NO_CONTENT
