

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from src.common.infrastructure.adapters.JWT_auth_handler import JWT_auth_handler
from src.common.infrastructure.config.database.database import get_db
from src.common.utils.verify_role import verify_roles
from src.orders.infrastructure.repositories.product_postgres_repository import Product_postgres_repository
from src.reports.application.services.get_revenue_by_product_service import GetProductRevenueService
from src.reports.application.services.get_sales_by_product_service import GetProductSalesService
from src.reports.application.services.get_top_customer_service import GetTopCustomersService
from src.reports.application.services.get_top_products_services import GetTopProductsService
from src.reports.application.services.get_total_revenue_servcie import GetTotalRevenueService
from src.reports.application.services.get_total_sales_service import GetTotalSalesService
from src.reports.infrastructure.repositories.reports_postgres_repository import ReportPostgresRepository


reports_routes = APIRouter(
    prefix='/orders',
)

auth = JWT_auth_handler()


@reports_routes.get('/sales/total',tags=['reports'],include_in_schema=False)
async def get_total_sales(
    response:Response,
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload = info.result()

    if not verify_roles(payload['role'],['MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    service = GetTotalSalesService(
        report_repository=ReportPostgresRepository(session),
    )
    result = await service.execute()
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return {
        'Total amount of sales': result.result()
    }


@reports_routes.get('/sales/{product_id}',tags=['reports'],include_in_schema=False)
async def get_sales_by_product(
    product_id,
    response:Response,
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload = info.result()

    if not verify_roles(payload['role'],['MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    
    service = GetProductSalesService(
        product_repository=Product_postgres_repository(session),
        report_repository=ReportPostgresRepository(session=session)
    )
    result = await service.execute(product_id)
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()

@reports_routes.get('/profit/total',tags=['reports'],include_in_schema=False)
async def get_total_profit(
    response:Response,
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload = info.result()

    if not verify_roles(payload['role'],['MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    service = GetTotalRevenueService(
        report_repository=ReportPostgresRepository(session=session),
    )
    result = await service.execute()
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()

@reports_routes.get('/profit/{product_id}',tags=['reports'],include_in_schema=False)
async def get_product_revenue(
    response:Response,
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload = info.result()

    if not verify_roles(payload['role'],['MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    service = GetProductRevenueService(
        product_repository=Product_postgres_repository(session),
        report_repository=ReportPostgresRepository(session=session),
    )
    result = await service.execute()
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()

@reports_routes.get('/products/top',tags=['reports'],include_in_schema=False)
async def get_top_products(
    response:Response,
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload = info.result()

    if not verify_roles(payload['role'],['MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    service = GetTopProductsService(
        report_repository=ReportPostgresRepository(session=session),
    )
    result = await service.execute()
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()

@reports_routes.get('/customer/top',tags=['reports'],include_in_schema=False)
async def get_customers_top(
    response:Response,
    session: Session = Depends(get_db), 
    info = Depends(auth.decode)
):
    if info.is_error():
        response.status_code = info.error.code
        return {'msg': info.get_error_message()}

    payload = info.result()

    if not verify_roles(payload['role'],['MANAGER']):
        response.status_code = 401
        return {'msg': 'This information is not accesible for this user' }
    
    service = GetTopCustomersService(
        report_repository=ReportPostgresRepository(session=session),
    )
    result = await service.execute()
    if result.is_error():
        response.status_code = result.error.code
        return {'msg': result.get_error_message() } 
    return result.result()