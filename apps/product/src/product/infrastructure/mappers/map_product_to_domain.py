from datetime import datetime
from src.product.application.schemas.product_schema import Product as ProductSchema
from src.product.domain.product import Product

def map_domain_to_product(product: ProductSchema) -> Product:
    return Product(
        code=product.code,
        name=product.name,
        description=product.description,
        cost=product.cost,
        margin=product.margin,
        price=product.price,
        quantity=product.quantity,
        created_at=product.created_at.isoformat(),
        updated_at=product.updated_at.isoformat()
    )