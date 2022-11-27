import json
from dataclasses import asdict
from datetime import datetime

from app.base.accessor import BaseManager
from app.store.users.users_accessor import User
from app.base.utils import do_by_timeout_wrapper
from app.store.jsonrpc.jsonrpc import JSON_RPC_RQ, JSON_RPC_RS  

class GeoClientMethod:
    INITIAL                 = 'initial'
    GET_ID                  = 'get_id'
    CREATE_GROUP            = 'create_group'
    SUBSCRIBE_TO_GROUP      = 'subscribe_to_group'
    START_METRONOME         = 'start_metronome'
    STOP_METRONOME          = 'stop_metronome'
    UPDATE_TEMP             = 'update_temp'
    PING                    = 'ping'



class GeoManager(BaseManager):
    class Meta:
        name = 'geo_manager'

    MAX_ERROR = 0.05

    async def handle(self, connection_id: str):
        await self._send_initial_rs(connection_id)
        # await self._send_test_data(connection_id)
        # await do_by_timeout_wrapper(
        #     callback=self._send_test_data(connection_id),
        #     timeout=5,
        #     args=[connection_id],
        # )
        async for rq in self.store.ws_accessor.stream(connection_id):
            should_continue = await self._handle_rq(rq, connection_id)
            if not should_continue:
                break

    async def _handle_rq(self, rq: JSON_RPC_RQ, connection_id: str) -> bool:
        if rq.method == GeoClientMethod.GET_ID:
            user = await self.store.users_accessor.add(
                connection_id=connection_id,
                name="default-name",
            )
            self.logger.info(f'New user saving: {user}')
            rs = JSON_RPC_RS(
                result={
                    "status": "success",
                    "client_id": user.client_id,
                },
                id=rq.id,
            )
            await self.store.ws_accessor.push(rs, connection_id=connection_id)
            return True
        elif rq.method == GeoClientMethod.CREATE_GROUP:
            user = await self.store.users_accessor.add(
                connection_id=connection_id,
                name="default-name",
            )
            self.logger.info(f'New user connected: {user}')
            payload = asdict(user)
            payload['id'] = connection_id
            rs = JSON_RPC_RS(
                # kind=GeoClientMethod.ADD,
                result=payload,
                id=rq.id,
            )
            await self.store.ws_accessor.broadcast(
                rs,
                except_of=[connection_id],
            )
            return True
        elif rq.method == GeoClientMethod.SUBSCRIBE_TO_GROUP:
            user = await self.store.users_accessor.get(connection_id=connection_id)
            self.logger.info(f'User {user} disconnected')
            await self.on_user_disconnect(connection_id)
            return True
        elif rq.method == GeoClientMethod.PING:
            user = await self.store.users_accessor.get(connection_id)
            latitude = rq.params['latitude']
            longitude = rq.params['longitude']

            if abs(user.latitude - latitude) > self.MAX_ERROR or abs(user.longitude - longitude) > self.MAX_ERROR:
                await self.store.ws_accessor.broadcast(
                    rs=JSON_RPC_RS(
                        # kind=GeoClientMethod.MOVE,
                        payload={
                            'id': user.client_id,
                            'latitude': latitude,
                            'longitude': longitude,
                        },
                        id=rq.id,
                    ),
                    except_of=[connection_id],
                )
                await self.store.users_accessor.update_coords(
                    connection_id=user.client_id,
                    latitude=latitude,
                    longitude=longitude,
                )
            return True
        elif rq.method == GeoClientMethod.UPDATE_TEMP:
            await self._send_test_data(connection_id)
            return True
        else:
            raise NotImplementedError

    async def _send_initial_rs(self, connection_id: str):
        rs: json = {"status":"success"}
        rs = JSON_RPC_RS(
            result=rs,
            id=None,
        )
        await self.store.ws_accessor.push(rs, connection_id=connection_id)

    async def _send_test_data(self, connection_id: str):
        rs = JSON_RPC_RS(
            result={
                "timestamp": f"{datetime.now().timestamp()}"
                , "date1 from python timestamp": f"{datetime.utcfromtimestamp(datetime.now().timestamp())}"
                , "date2 from int timestamp": f"{datetime.utcfromtimestamp(round(datetime.now().timestamp() * 1000) / 1e3)}"
            },
            id=None,
        )
        await self.store.ws_accessor.push(rs, connection_id=connection_id)

    async def on_user_disconnect(self, connection_id: str) -> None:
        await self.store.users_accessor.remove(connection_id)
        await self.store.ws_accessor.broadcast(
            rs=JSON_RPC_RS(
                result={
                    'id': connection_id,
                },
                id=None,
            ),
            except_of=[connection_id],
        )
