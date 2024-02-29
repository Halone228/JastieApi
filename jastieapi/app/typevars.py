from jastiedatabase.sql import *
from fastapi import Depends
from typing import Annotated, TypeAliasType


users_db_typevar = Annotated[UserDBHelper, Depends(get_helper(UserDBHelper), use_cache=False)]
matches_db_typevar = Annotated[MatchesDBHelper, Depends(get_helper(MatchesDBHelper), use_cache=False)]
logs_db_typevar = Annotated[LogsDBHelper, Depends(get_helper(LogsDBHelper), use_cache=False)]
vendors_db_typevar = Annotated[VendorDBHelper, Depends(get_helper(VendorDBHelper), use_cache=False)]


