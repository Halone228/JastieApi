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
        message=data.message,
        session=session
    )
    data = await new_vendor.execute()
    return list(data)
