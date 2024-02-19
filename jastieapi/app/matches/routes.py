from pydantic import BaseModel, AwareDatetime, Field
from jastieapi.app.include import *
from jastiedatabase.datamodels import Match, Bid


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
    url: str


class BidCreate(BaseModel):
    match_id: int
    bid: float
    first_select: bool


matches_router = APIRouter(
    prefix='/matches',
    tags=['Matches']
)


@matches_router.get('/active_matches')
async def get_active_matches(
    matches_db_helper: matches_db_typevar
) -> list[Match]:
    data = await matches_db_helper.get_active_matches()
    return [Match.model_validate(i, from_attributes=True) for i in data]


@matches_router.get('/all')
async def get_all_matches(
    matches_db_helper: matches_db_typevar
) -> list[Match]:
    data = await matches_db_helper.get_all_matches()
    return [Match.model_validate(i, from_attributes=True) for i in data]


@matches_router.get('/{match_id}')
async def get_match(
    match_id: int,
    matches_db_helper: matches_db_typevar
) -> Match | None:
    data = await matches_db_helper.get_match(match_id)
    return data


@matches_router.get('/bids/{user_id}')
async def get_user_bids(
    user_id: int,
    matches_db_helper: Annotated[MatchesDBHelper, Depends(get_helper(MatchesDBHelper))]
) -> list[Bid]:
    data = await matches_db_helper.get_user_bids(user_id)
    return [Bid.model_validate(i, from_attributes=True) for i in data]


@matches_router.post('/bid/create/{user_id}')
async def create_bid(
    bid: BidCreate,
    user_id: int,
    matches_db_helper: matches_db_typevar
):
    await matches_db_helper.set_bid_for_match(
        match_id=bid.match_id,
        user_id=user_id,
        first_select=bid.first_select,
        bid=bid.bid
    )


@matches_router.post('/match/create')
async def create_match(
    match: MatchCreate,
    matches_db_helper: Annotated[MatchesDBHelper, Depends(get_helper(MatchesDBHelper))]
):
    await matches_db_helper.create_match(match)


@matches_router.get('/match/{match_id}/win/{first_team}')
async def set_win(
    match_id: int,
    first_team: bool,
    matches_db_helper: matches_db_typevar,
    user_db_helper: users_db_typevar
):
    bids = await matches_db_helper.get_match_bids(match_id)
    await matches_db_helper.set_match_win(
        match_id=match_id,
        first_win=first_team
    )
    match = await matches_db_helper.get_match(match_id)
    for bid in bids:
        await user_db_helper.add_points(
            user_id=bid.user_id,
            value=(match.first_coff if bid.first_select else match.second_coff)*bid.bid,
            by='bid'
        )




