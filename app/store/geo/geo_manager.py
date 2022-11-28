import json
from dataclasses import asdict
from datetime import datetime

from utils.Utils import Utils
from app.base.accessor import BaseManager
from app.store.users.users_accessor import User
from app.base.utils import do_by_timeout_wrapper
from app.store.jsonrpc.jsonrpc import JSON_RPC_BASE, JSON_RPC_RQ, JSON_RPC_RS  

class GeoClientMethod:
    INITIAL                 = 'initial'
    GET_ID                  = 'get_id'
    CREATE_GROUP            = 'create_group'
    SUBSCRIBE_TO_GROUP      = 'subscribe_to_group'
    START_METRONOME         = 'start_metronome'
    UPDATE_TEMP             = 'update_temp'
    STOP_METRONOME          = 'stop_metronome'
    DISCONNECT              = 'disconnect'
    PING                    = 'ping'

class GeoServerMethod:
    PLAY_SOUND              = 'play_sound'
    STOP_SOUND              = 'stop_sound'
    


class GeoManager(BaseManager):
    class Meta:
        name = 'geo_manager'

    MAX_ERROR = 0.05

    async def handle(self, connection_id: str):
        await self._sendInitialData(connection_id)
        async for data in self.store.wsAccessor.stream(connection_id):
            should_continue = await self._handleInputData(data, connection_id)
            if not should_continue:
                break

    async def _handleInputData(self, data: JSON_RPC_BASE, connection_id: str) -> bool:
        if type(data).__name__ == 'JSON_RPC_RQ':
            return await self._handleRQ(data, connection_id)
        else:
            return await self._handleRS(data, connection_id)

    async def _handleRQ(self, rq: JSON_RPC_RQ, connection_id: str) -> bool:
        rs: JSON_RPC_RS = JSON_RPC_RS(result={"status":"error","message":"request error"}, id=rq.id)
        if rq.method == GeoClientMethod.GET_ID:
            user = await self.store.usersAccessor.addUser(
                connection_id=connection_id,
                name="default-name",
            )
            rs = JSON_RPC_RS(
                result={
                    "status": "success",
                    "client_id": user.client_id,
                },
                id=rq.id,
            )
        elif rq.method == GeoClientMethod.CREATE_GROUP:
            user = await self.store.usersAccessor.getUser(connection_id=connection_id)
            if user is not None:
                group = await self.store.groupAccessor.createGroup(userOwner=user)
                rs = JSON_RPC_RS(
                    result={
                        "status": "success",
                        "group_id": group.userOwner.client_id,
                    },
                    id=rq.id,
                )
        elif rq.method == GeoClientMethod.SUBSCRIBE_TO_GROUP:
            user = await self.store.usersAccessor.getUser(connection_id=connection_id)
            if user is not None:
                group = await self.store.groupAccessor.addUserToGroup(user, group_id=rq.params['group_id'])
                rs = JSON_RPC_RS(
                    result={
                        "status": ("error" if group == None else "success"),
                    },
                    id=rq.id,
                )
        elif rq.method == GeoClientMethod.START_METRONOME:
            user = await self.store.usersAccessor.getUser(connection_id=connection_id)
            if user is not None:
                rs = JSON_RPC_RS(
                    result={
                        "status": "success",
                    },
                    id=rq.id,
                )
                await self.store.wsAccessor.push(data=rs, connection_id=connection_id)

                listUsersToSend = [user.connection_id]
                rqToGroup = JSON_RPC_RQ(
                    method=GeoServerMethod.PLAY_SOUND,
                    params={"start_ts":Utils.getCurrentTimestampMs()+2000,"bpm":120},
                    id=Utils.getCurrentTimestampMs(),
                )
                group = await self.store.groupAccessor.getGroup(group_id=user.client_id)
                if group is not None:
                    for user in group.subscribedUsers:
                        listUsersToSend.append(user.connection_id)
                await self.store.wsAccessor.broadcast(rqToGroup,listUsersToSend)
            return True
        elif rq.method == GeoClientMethod.UPDATE_TEMP:
            await self._send_test_data(connection_id)
        elif rq.method == GeoClientMethod.STOP_METRONOME:
            user = await self.store.usersAccessor.getUser(connection_id=connection_id)
            if user is not None:
                rs = JSON_RPC_RS(
                    result={
                        "status": "success",
                    },
                    id=rq.id,
                )
                await self.store.wsAccessor.push(data=rs, connection_id=connection_id)

                listUsersToSend = [user.connection_id]
                rqToGroup = JSON_RPC_RQ(
                    method=GeoServerMethod.STOP_SOUND,
                    params=None,
                    id=Utils.getCurrentTimestampMs(),
                )
                group = await self.store.groupAccessor.getGroup(group_id=user.client_id)
                if group is not None:
                    for user in group.subscribedUsers:
                        listUsersToSend.append(user.connection_id)
                await self.store.wsAccessor.broadcast(rqToGroup,listUsersToSend)
            return True
        else:
            raise NotImplementedError

        await self.store.wsAccessor.push(data=rs, connection_id=connection_id)
        return True

    async def _handleRS(self, rs: JSON_RPC_RS, connection_id: str) -> bool:
        self.logger.info(f'_handleRS {rs=}, {connection_id=}')
            
    async def _sendInitialData(self, connection_id: str):
        rs: json = {"status":"success"}
        rs = JSON_RPC_RS(
            result=rs,
            id=None,
        )
        await self.store.wsAccessor.push(rs, connection_id=connection_id)

    async def _send_test_data(self, connection_id: str):
        rs = JSON_RPC_RS(
            result={
                "timestamp": f"{datetime.now().timestamp()}"
                , "date1 from python timestamp": f"{datetime.utcfromtimestamp(datetime.now().timestamp())}"
                , "date2 from int timestamp": f"{datetime.utcfromtimestamp(round(datetime.now().timestamp() * 1000) / 1e3)}"
            },
            id=None,
        )
        await self.store.wsAccessor.push(rs, connection_id=connection_id)

    async def _sendRQToClient(self, rq: JSON_RPC_RQ, connection_id: str):
        await self.store.wsAccessor.push(data=rq, connection_id=connection_id)

    async def on_user_disconnect(self, connection_id: str) -> None:
        user = await self.store.usersAccessor.getUser(connection_id)
        if user is None:
            await self.store.groupAccessor.removeUserFromAllGroups(user)
            await self.store.usersAccessor.removeUser(connection_id)
