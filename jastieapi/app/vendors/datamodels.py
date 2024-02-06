import aiogram.types
from pydantic import BaseModel


class VendorRequest(BaseModel):
    vendor: str
    action: str
    data: str
    message: aiogram.types.Message
