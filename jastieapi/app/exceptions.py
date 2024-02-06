from fastapi import HTTPException, status


CHAT_DISALLOWED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='chat_disallowed'
)

__all__ = [
    'CHAT_DISALLOWED'
]