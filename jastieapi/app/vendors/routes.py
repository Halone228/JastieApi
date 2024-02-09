from jastieapi.app.include import *
from .datamodels import VendorRequest
from .callbacks import vendors


vendors_route = APIRouter(
    prefix='/vendors',
    tags=['Vendors']
)


@vendors_route.post('/vendor')
async def process_vendor(data: VendorRequest, session: Annotated[AsyncSession, Depends(get_session)]):
    vendor = vendors[data.vendor]
    new_vendor = vendor(
        action=data.action,
        data=data.data,
        user_id=data.user_id,
        full_name=data.full_name,
        username=data.username,
        session=session
    )
    data = await new_vendor.execute()
    return {'data': list(data)}
