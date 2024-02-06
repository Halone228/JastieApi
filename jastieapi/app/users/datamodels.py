from pydantic import BaseModel


class Points(BaseModel):
    points: float
    user_id: int