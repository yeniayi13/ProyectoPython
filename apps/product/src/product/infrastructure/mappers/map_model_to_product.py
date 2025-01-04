from src.product.application.schemas.product_schema import Product
from src.product.infrastructure.models.product_model import ProductModel


def model_to_product(product_model: ProductModel) -> Product:
    return Product(
        id=product_model.id,
        code=product_model.code,
        name=product_model.name,
        description=product_model.description,
        cost=product_model.cost,
        margin=product_model.margin,
        price=product_model.price,
        quantity=product_model.quantity,
        created_at=product_model.created_at,
        updated_at=product_model.updated_at,
    )