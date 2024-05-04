from jastiedatabase.sql import Messages, UserPoints, asession_maker
from asyncio import run
from sqlalchemy import select, update
from functools import reduce

points = {
    6117709352: 7500,
    5147743068: 3500,
    629580593: 20000,
    992323260: 3700,
    744651251: 1500,
    1740004351: 5500,
    1995069812: 3200,
    830751624: 3200,
    6823469850: 500,
    932205679: 2800,
    499435454: 3000,
    871043272: 2500,
    5898951369: 3500,
    6743468873: 1,
    1198124194: 1900
}


async def main():
    async with asession_maker() as session:
        result = await session.execute(select(Messages).where(Messages.id >= 449589))

        def _cumm(cumm_val: dict, new_val: Messages):
            cumm_val[new_val.user_id] = len(new_val.text) + cumm_val.get(new_val.user_id, 0)
            return cumm_val

        data = reduce(_cumm, result.scalars(), {})

        for k in points:
            points[k] += data[k] / 100
        print(points)
        # await session.execute(
        #     update(UserPoints),
        #     [
        #         {'user_id': k, 'points': points[k]}
        #         for k in points
        #     ]
        # )
        # await session.commit()


run(main())
