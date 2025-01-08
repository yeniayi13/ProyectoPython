
from src.common.application.ports.request_handler import Request_handler
import httpx
from src.common.infrastructure.config.config import get_settings
from src.common.utils.errors import Error
from src.common.utils.result import Result
settings = get_settings()

class Httpx_request_handler(Request_handler):
    
    
    async def discount_product_quantity(self, route:str, product_id: str, quantity: str ) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.put(f"{route}/{product_id}/{quantity}")
                print(response)
                if response.status_code == 500:
                    response_payload ={
                        'code': 500, 
                        'msg': 'There is a problem within product service'
                    }
                else:
                    response_payload = response.json()

                return response_payload
            except httpx.HTTPStatusError as e:
                print('httpx.HTTPStatusError:',e)
                #Result.failure(Error(),'','')
                #Result.failure(Error(),'','')raise HTTPException(
                #Result.failure(Error(),'','')    status_code=e.response.status_code,
                #Result.failure(Error(),'','')    detail=e.response.json().get("detail", "Unknown error")
                #)


    async def replenish_cancelled_products(self,route: str, products:dict) -> str:
        async with httpx.AsyncClient() as client:
            try:
                #print('products:', products)
                response = await client.put(
                    f"http://localhost:8001/inventories/replenish_products/", 
                    json=products)
                #print(client.headers)
                #print(response.headers)
                #print(response)
                #print(response.text)
                if response.status_code == 500:
                    response_payload ={
                        'code': 500, 
                        'msg': 'There is a problem within product service'
                    }
                else:
                    response_payload = response.json()

                return response_payload
            except httpx.HTTPStatusError as e:
                print('httpx.HTTPStatusError:',e)
                #Result.failure(Error(),'','')
                #Result.failure(Error(),'','')raise HTTPException(
                #Result.failure(Error(),'','')    status_code=e.response.status_code,
                #Result.failure(Error(),'','')    detail=e.response.json().get("detail", "Unknown error")
                #)
    