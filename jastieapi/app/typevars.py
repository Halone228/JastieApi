from jastie_database.sql import *
from fastapi import Depends
from typing import Annotated, TypeAliasType


users_db_typevar = Annotated[UserDBHelper, Depends(get_helper(UserDBHelper))]
matches_db_typevar = Annotated[MatchesDBHelper, Depends(get_helper(MatchesDBHelper))]


