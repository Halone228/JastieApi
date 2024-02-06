from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from jastieapi.app.include import *


class BaseVendor(ABC):
    def __init__(
            self,
            action: str,
            data: str,
            message: aiogram_types.Message,
            session: AsyncSession
    ):
        self.action = action
        self.data = self._parse_data(data)
        self.message = message
        self.session = session

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


class SkinVendor(BaseVendor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_helper = UserDBHelper(self.session)
        self.skin = None

    async def get_info(self) -> tuple[str, bool]:
        skin_id: int = int(self.data.get('skin_id', -1))
        skin = await get_skin_by_id(skin_id)
        self.skin = skin
        if skin is None:
            return "Такого скина нет.", False
        points = await self.user_helper.get_points(self.message.from_user.id)
        if points >= skin.price:
            return (f"Скин {skin.item_name} куплен.\nСпасибо за покупку 🤑\n"
                    f"Переходите к @jastie777\nИ забирай свою покупку 🔥") , True
        else:
            return "Недостаточно баллов.", False

    async def execute(self) -> tuple[str, bool]:
        info = await self.get_info()
        to_execute = info[1]
        if to_execute:
            await self.user_helper.add_points(self.message.from_user.id, value=self.skin.price*SKIN_MULTIPLIER)
            return info
        return info

    async def close(self):
        await super().close()
        await self.user_helper.close()


vendors: dict[str, Type[BaseVendor]] = {
    'skin': SkinVendor
}