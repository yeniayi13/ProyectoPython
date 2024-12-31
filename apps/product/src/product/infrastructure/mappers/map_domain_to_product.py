from datetime import datetime
from src.product.application.schemas.product_schema import Product as ProductSchema
from src.product.domain.product import Product

def map_domain_to_product(product: Product) -> ProductSchema:
    return Product(
        id=product.id,
        code=product.code,
        name=product.name,
        description=product.description,
        cost=product.cost,
        margin=product.margin,
        price=product.price,
        quantity=product.quantity,
        created_at=datetime.fromisoformat(product.created_at),
        updated_at=datetime.fromisoformat(product.updated_at)
    )