from pydantic import BaseModel


class Cancel_order_entry(BaseModel):
    order_id:str
    