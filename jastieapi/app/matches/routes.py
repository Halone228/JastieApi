from asyncio import gather

from pydantic import BaseModel, AwareDatetime, Field
from jastieapi.app.include import *
from jastiedatabase.datamodels import Match, Bid
from .methods import send_messages


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
    RunnerSaver.create_task(matches_db_helper.set_bid_for_match(
        match_id=bid.match_id,
        user_id=user_id,
        first_select=bid.first_select,
        bid=bid.bid
    ))


@matches_router.post('/match/create')
async def create_match(
    match: MatchCreate,
    matches_db_helper: Annotated[MatchesDBHelper, Depends(get_helper(MatchesDBHelper))]
):
    RunnerSaver.create_task(matches_db_helper.create_match(match))


@matches_router.get('/match/{match_id}/win/{first_team}')
async def set_win(
    match_id: int,
    first_team: bool,
    matches_db_helper: matches_db_typevar,
    user_db_helper: users_db_typevar
):
    tasks = []
    bids = await matches_db_helper.get_match_bids(match_id)
    tasks.append(matches_db_helper.set_match_win(
        match_id=match_id,
        first_win=first_team
    ))
    match = await matches_db_helper.get_match(match_id)
    coff = match.first_coff if first_team else match.second_coff
    points = {bid.user_id: bid.bid*coff for bid in bids if bid.first_select == first_team}
    tasks.append(user_db_helper.add_points_bulk(
        ids_values=points,
        by='bid_result'
    ))
    users_message: dict = {
        bid.user_id:
        f'Матч {match.match_name}.\n'
        f'Победа за {match.first_opponent if first_team else match.second_opponent}\n'
        f'Ваша ставка ({bid.bid:.2f}) была на {match.first_opponent if bid.first_select else match.second_opponent}'
        for bid in bids
    }
    tasks.append(
        send_messages(users_message)
    )
    RunnerSaver.create_task(gather(*tasks))





