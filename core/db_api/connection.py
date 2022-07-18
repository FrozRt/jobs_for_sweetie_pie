import asyncio
from typing import List, Optional, Type, TypeVar, Union

import aiomysql
from loguru import logger

from settings.config import settings

from . import misc

T = TypeVar("T")


class RawConnection:
    connection_pool = None

    @staticmethod
    async def _make_request(
        sql: str,
        params: Union[tuple, List[tuple]] = None,
        fetch: bool = False,
        mult: bool = False,
        retries_count: int = 5,
        model_type: Type[T] = None,
    ) -> Optional[Union[List[T], T]]:
        if RawConnection.connection_pool is None:
            RawConnection.connection_pool = await aiomysql.create_pool(
                **settings.get_db_connection_data()
            )
        async with RawConnection.connection_pool.acquire() as conn:
            conn: aiomysql.Connection
            async with conn.cursor(aiomysql.DictCursor) as cur:
                cur: aiomysql.DictCursor
                for i in range(retries_count):
                    try:
                        if isinstance(params, list):
                            await cur.executemany(sql, params)
                        else:
                            await cur.execute(sql, params)
                    except (aiomysql.OperationalError, aiomysql.InternalError) as e:
                        if "Deadlock found" in str(e):
                            await asyncio.sleep(1)
                    else:
                        break
                if fetch:
                    if mult:
                        r = await cur.fetchall()
                    else:
                        r = await cur.fetchone()
                    if model_type is not None:
                        try:
                            return misc.convert_to_model(r, model_type)
                        except Exception as e:
                            logger.error(e)
                            return r
                    else:
                        return r
                else:
                    await conn.commit()
