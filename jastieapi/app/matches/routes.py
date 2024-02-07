from pydantic import BaseModel, AwareDatetime, Field
from jastieapi.app.include import *
from jastie_database.datamodels import Match, Bid


class MatchCreate(BaseModel):
    first_opponent: str
    second_opponent: str
    match_name: str
    first_coff: float = Field(
        gt=1
    )
    second_coff: float = Field(
        gt=1
    )
    end_time: AwareDatetime


class BidCreate(BaseModel):
    match_id: int
    bid: float
    first_win: bool


matches_router = APIRouter(
    prefix='/matches',
    tags=['Matches']
)


@matches_router.get('/active_matches')
async def get_active_matches(
    matches_db_helper: Annotated[MatchesDBHelper, Depends(get_helper(MatchesDBHelper))]
) -> list[Match]:
    data = await matches_db_helper.get_active_matches()
    return [Match.model_validate(i, from_attributes=True) for i in data]


@matches_router.get('/bids/{user_id}')
async def get_user_bids(
    user_id: int,
    matches_db_helper: Annotated[MatchesDBHelper, Depends(get_helper(MatchesDBHelper))]
) -> list[Bid]:
    data = await matches_db_helper.get_user_bids(user_id)
    return [Bid.model_validate(i, from_attributes=True) for i in data]


@matches_router.post('/match/create')
async def create_match(
    match: MatchCreate,
    matches_db_helper: Annotated[MatchesDBHelper, Depends(get_helper(MatchesDBHelper))]
):
    await matches_db_helper.create_match(match)



