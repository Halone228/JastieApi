from pydantic import BaseModel


class TextMessage(BaseModel):
    text: str


__all__ = [
    'TextMessage'
]
