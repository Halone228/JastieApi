from enum import Enum


class UsersResultCodes(Enum):
    SUCCESS = 1
    REFERRER_ALREADY_EXISTS = -3
    USER_NOT_FOUND = -403
    REFERRER_SELF = -4
