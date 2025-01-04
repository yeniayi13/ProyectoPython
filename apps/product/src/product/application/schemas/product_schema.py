from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, validator, root_validator

class ProductQuantityUpdate(BaseModel):
    quantity: int = Field(..., ge=0, description="Nueva cantidad del producto")

class ProductBase(BaseModel):
    code: str = Field(..., min_length=3, max_length=20, description="Código del producto")
    name: str = Field(..., min_length=2, max_length=100, strip_whitespace=True, description="Nombre del producto")
    description: str = Field(..., min_length=5, max_length=500, strip_whitespace=True, description="Descripción detallada del producto")
    cost: float = Field(..., gt=0, description="Costo del producto, debe ser mayor que cero")
    margin: float = Field(..., gt=0, lt=1, description="Margen de ganancia, debe ser mayor que cero y menor que uno")
    price: float = Field(..., gt=0, description="Precio de venta, debe ser mayor que cero")
    quantity: int = Field(..., ge=0, description="Cantidad en stock, debe ser mayor o igual que cero")
    
    @validator('code')
    def code_must_be_alphanumeric(cls, value):
        if not value.isalnum():
            raise ValueError('El código debe ser alfanumérico')
        return value

class ProductCreate(ProductBase):
    @root_validator(pre=True)
    def calculate_price(cls, values):
        cost = values.get('cost')
        margin = values.get('margin')
        if cost is not None and margin is not None:
            if margin >= 1:
                raise ValueError("El margen debe ser menor que 1 para calcular el precio")
            values['price'] = round(cost / (1 - margin), 2)
        return values

class ProductUpdate(BaseModel):
    id: UUID = Field(...) # Se requiere el id
    code: Optional[str] = Field(None, description="Código del producto")
    name: Optional[str] = Field(None, description="Nombre del producto")
    description: Optional[str] = Field(None, description="Descripción detallada del producto")
    cost: Optional[float] = Field(None, description="Costo del producto, debe ser mayor que cero")
    margin: Optional[float] = Field(None, description="Margen de ganancia, debe ser mayor o igual que cero")
    price: Optional[float] = Field(None, description="Precio de venta, debe ser mayor que cero")
    quantity: Optional[int] = Field(None, description="Cantidad en stock, debe ser mayor o igual que cero")

class Product(ProductBase):
    id: UUID = Field(default_factory=UUID)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    class Config:
        json_encoders = {
            UUID: lambda u: str(u),  # Convierte UUID a string al serializar a JSON
        }

        @staticmethod
        def json_loads(json_str: str) -> dict:
            import json
            data = json.loads(json_str)
            # Convierte strings UUID a objetos UUID al deserializar desde JSON
            if "id" in data:
                data["id"] = UUID(data["id"])
            return data

class ProductResponse(Product):
    class Config:
        from_attributes = True
