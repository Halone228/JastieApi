from pydantic import BaseModel

from jastiedatabase.datamodels import Vendor


class VendorRequest(BaseModel):
    vendor: str
    action: str
    data: str
    user_id: int
    username: str
    full_name: str


class VendorsData(BaseModel):
    result: list[Vendor]
    page: int
