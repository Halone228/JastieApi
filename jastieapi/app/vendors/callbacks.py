from abc import ABC, abstractmethod
from typing import Type
from typing import Callable, Coroutine, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from jastieapi.app.include import *


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

    @staticmethod
    def _parse_data(data: str) -> dict[str, str]:
        return {
            i[0]: i[1] for i in [
                k.split(':') for k in data.split('-')
            ] if len(i) == 2}

    @abstractmethod
    async def get_info(self):
        pass

    @abstractmethod
    async def execute(self):
        pass

    async def close(self):
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
    async def get_info(self) -> tuple[str, bool, _async_function, str]:
        pass

    async def execute(self) -> tuple[str, bool]:
        info = await self.get_info()
        to_execute = info[1]
        result = info[0], info[1]
        if to_execute and len(info) == 4:
            await info[2]()
            return result
        return result


class SkinVendor(BuyVendor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skin = None
        logger.debug(self.data)

    async def get_info(self) -> tuple[str, bool, _async_function, str] | tuple[str, bool]:
        skin_id: int = int(self.data.get('skin_id', -1))
        skin = await get_skin_by_id(skin_id)
        self.skin = skin
        if skin is None:
            return "Такого скина нет.", False
        can = await self.buy(skin.price*SKIN_MULTIPLIER)
        if can:
            async def callback():
                await self.user_helper.add_points(self.user_id, -skin.price*SKIN_MULTIPLIER)

            return ((f"Скин {skin.item_name} куплен.\nСпасибо за покупку 🤑\n"
                    f"Переходите к @jastie777\nИ забирай свою покупку 🔥"), can,
                    callback, skin.item_name)
        else:
            return "Недостаточно баллов.", can

    async def close(self):
        await super().close()
        await self.user_helper.close()


class DiscountVendor(BuyVendor):
    async def get_info(self) -> tuple[str, bool, _async_function, str] | tuple[str, bool]:
        discount = await get_discount(self.data.get('discount_name'))

        can = await self.buy(discount.price)
        if can:
            async def callback():
                await self.user_helper.add_points(self.user_id, -discount.price)

            return ((f"Спасибо за покупку 🤑\n"
                     f"Переходите к @jastie777\nИ забирай свою покупку 🔥"), can,
                    callback, discount.name)
        else:
            return "Недостаточно баллов.", can

    async def close(self):
        await super().close()
        await self.user_helper.close()


vendors: dict[str, Type[BaseVendor]] = {
    'skin': SkinVendor,
    'discount': DiscountVendor
}
