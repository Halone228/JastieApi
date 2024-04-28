from abc import ABC, abstractmethod
from typing import Type
from typing import Callable, Coroutine, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from jastieapi.app.include import *
from loguru import logger

_async_function = Optional[Callable[[], Coroutine[Any, Any, None]]]


class BaseVendor(ABC):
    def __init__(
        self,
        action: str,
        data: str,
        user_id: int,
        username: str,
        full_name: str,
        session: AsyncSession
    ):
        self.action = action
        self.data = self._parse_data(data)
        self.user_id = user_id
        self.session = session
        self.username = username
        self.full_name = full_name
        self.logs_helper = LogsDBHelper(self.session)
        self.logger = logger.bind(
            name='vendor',
            user_id=self.user_id
        )

    @staticmethod
    def _parse_data(data: str) -> dict[str, str]:
        return {
            i[0]: i[1] for i in [
                k.split(':') for k in data.split('-')
            ] if len(i) == 2}

    @property
    def vendor_name(self):
        return self.__class__.__name__.lower().replace('vendor', '')

    @abstractmethod
    async def get_info(self):
        pass

    @abstractmethod
    async def execute(self):
        pass

    async def close(self):
        await self.logs_helper.close()
        await self.session.close()


class BuyVendor(BaseVendor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_helper = UserDBHelper(self.session)

    async def buy(self, price: float):
        points = await self.user_helper.get_points(self.user_id)
        logger.debug(points)
        return points >= price

    @abstractmethod
    async def get_info(self) -> tuple[str, bool, _async_function, dict]:
        pass

    async def execute(self) -> tuple[str, bool]:
        info = await self.get_info()
        to_execute = info[1]
        result = info[0], info[1]
        if to_execute and len(info) == 4:
            await info[2]()
            id = await self.logs_helper.add_vendor_transaction(
                vendor=self.vendor_name,
                action='buy',
                data=info[3],
                user_id=self.user_id
            )
            self.logger.info(
                f'transaction_id:{id}'
            )
            return result
        return result


class SkinVendor(BuyVendor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skin = None

    async def get_info(self) -> tuple[str, bool, _async_function, dict] | tuple[str, bool]:
        skin_id: int = int(self.data.get('skin_id', -1))
        skin = await get_skin_by_id(skin_id)
        self.skin = skin
        if skin is None:
            return "Такого скина нет.", False
        can = await self.buy(skin.price * SKIN_MULTIPLIER)
        if can:
            async def callback():
                await self.user_helper.add_points(self.user_id, -skin.price * SKIN_MULTIPLIER, by='vendor')

            return ((f"Скин {skin.item_name} куплен.\nСпасибо за покупку 🤑\n"
                     f"Переходите к @jastieboss\nИ забирай свою покупку 🔥"), can,
                    callback, {'item_name': skin.item_name})
        else:
            return "Недостаточно баллов.", can

    async def close(self):
        await super().close()
        await self.user_helper.close()


class DiscountVendor(BuyVendor):
    async def get_info(self) -> tuple[str, bool, _async_function, dict] | tuple[str, bool]:
        discount = await get_discount(self.data.get('discount_name'))

        can = await self.buy(discount.price)
        if can:
            async def callback():
                await self.user_helper.add_points(self.user_id, -discount.price, by='vendor')

            return ((f"Спасибо за покупку 🤑\n"
                     f"Переходите к @jastie777\nИ забирай свою покупку 🔥"), can,
                    callback, {'discount_name': discount.name})
        else:
            return "Недостаточно баллов.", can

    async def close(self):
        await super().close()
        await self.user_helper.close()


vendors: dict[str, Type[BaseVendor]] = {
    'skin': SkinVendor,
    'discount': DiscountVendor
}
