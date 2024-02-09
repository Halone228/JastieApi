import aiogram.types
from pydantic import BaseModel


class VendorRequest(BaseModel):
    vendor: str
    action: str
    data: str
    user_id: int
    username: str
    full_name: str
