from jastieapi.app.include import *
from .datamodels import VendorRequest, VendorsData
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


@vendors_route.get('/all')
async def get_all(
    vendor_db_helper: vendors_db_typevar,
    limit: int = 40,
    page: int = 0
):
    data = await vendor_db_helper.get_all_vendors(limit, page)
    return VendorsData.model_validate(
        {
            'page': page,
            'result': data
        }, from_attributes=True, strict=False
    )
