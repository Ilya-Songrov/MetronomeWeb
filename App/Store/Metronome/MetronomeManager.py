import typing
from dataclasses import asdict
from datetime import datetime

from Utils.Utils import Utils
from App.Base.Accessor import BaseManager
from App.Store.Users.UsersAccessor import User
from App.Base.Utils import doByTimeoutWrapper
from App.Store.jsonrpc.jsonrpc import JSON_RPC_BASE, JSON_RPC_RQ, JSON_RPC_RS  

class MetronomeClientMethod:
    GET_ID                  = 'get_id'
    CREATE_GROUP            = 'create_group'
    SUBSCRIBE_TO_GROUP      = 'subscribe_to_group'
    START_METRONOME         = 'start_metronome'
    UPDATE_TEMP             = 'update_temp'
    STOP_METRONOME          = 'stop_metronome'
    DISCONNECT              = 'disconnect'
    PING                    = 'ping'

class MetronomeServerMethod:
    GET_TIME                = 'get_time'
    PLAY_SOUND              = 'play_sound'
    STOP_SOUND              = 'stop_sound'
    


class MetronomeManager(BaseManager):
    class Meta:
        name = 'metronome_manager'

    def _init_(self) -> None:
        self._callbacksOnClientRS: dict[int, typing.Callable[['JSON_RPC_RS', str], typing.Awaitable]] = {}
        self._calcDifferenceInTsMs: dict[str, int] = {}

    async def handle(self, connection_id: str):
        self._calcDifferenceInTsMs[connection_id] = Utils.getCurrentTsMs()
        await self.store.usersAccessor.addUser(connection_id=connection_id)
        await self._sendRQ_GET_TIME(connection_id)
        async for data in self.store.wsAccessor.streamData(connection_id):
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
        if rq.method == MetronomeClientMethod.GET_ID:
            user = await self.store.usersAccessor.getUser(connection_id=connection_id)
            if user is not None:
                rs = JSON_RPC_RS(
                    result={
                        "status": "success",
                        "client_id": user.client_id,
                    },
                    id=rq.id,
                )
        elif rq.method == MetronomeClientMethod.CREATE_GROUP:
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
        elif rq.method == MetronomeClientMethod.SUBSCRIBE_TO_GROUP:
            user = await self.store.usersAccessor.getUser(connection_id=connection_id)
            if user is not None:
                group = await self.store.groupAccessor.addUserToGroup(user, group_id=rq.params['group_id'])
                rs = JSON_RPC_RS(
                    result={
                        "status": ("error" if group == None else "success"),
                        "message": ("group is not exist" if group == None else None),
                    },
                    id=rq.id,
                )
        elif rq.method == MetronomeClientMethod.START_METRONOME:
            user = await self.store.usersAccessor.getUser(connection_id=connection_id)
            if user is not None:
                rs = JSON_RPC_RS(
                    result={
                        "status": "success",
                    },
                    id=rq.id,
                )
                await self.store.wsAccessor.pushData(data=rs, connection_id=connection_id)

                listIdData: list[tuple[JSON_RPC_BASE,str]] = []
                rqUser = JSON_RPC_RQ(
                    method=MetronomeServerMethod.PLAY_SOUND,
                    params={"start_ts":Utils.getCurrentTsMs()+1000-user.differenceInTsMs,"bpm":120},
                    id=Utils.getNextId(),
                )
                listIdData.append([rqUser, user.connection_id])
                group = await self.store.groupAccessor.getGroup(group_id=user.client_id)
                if group is not None:
                    for user in group.subscribedUsers:
                        rqUser = JSON_RPC_RQ(
                            method=MetronomeServerMethod.PLAY_SOUND,
                            params={"start_ts":Utils.getCurrentTsMs()+1000-user.differenceInTsMs,"bpm":120},
                            id=Utils.getNextId(),
                        )
                        listIdData.append([rqUser, user.connection_id])
                await self.store.wsAccessor.broadcast(id_data=listIdData)
            return True
        elif rq.method == MetronomeClientMethod.UPDATE_TEMP:
            await self._sendTestDataRS(connection_id)
        elif rq.method == MetronomeClientMethod.STOP_METRONOME:
            user = await self.store.usersAccessor.getUser(connection_id=connection_id)
            if user is not None:
                rs = JSON_RPC_RS(
                    result={
                        "status": "success",
                    },
                    id=rq.id,
                )
                await self.store.wsAccessor.pushData(data=rs, connection_id=connection_id)

                listIdData: list[tuple[JSON_RPC_BASE,str]] = []
                rqUser = JSON_RPC_RQ(
                    method=MetronomeServerMethod.STOP_SOUND,
                    params=None,
                    id=Utils.getNextId(),
                )
                listIdData.append([rqUser, user.connection_id])
                group = await self.store.groupAccessor.getGroup(group_id=user.client_id)
                if group is not None:
                    for user in group.subscribedUsers:
                        listIdData.append([rqUser, user.connection_id])
                await self.store.wsAccessor.broadcast(id_data=listIdData)
            return True
        else:
            raise NotImplementedError

        await self.store.wsAccessor.pushData(data=rs, connection_id=connection_id)
        return True

    async def _handleRS(self, rs: JSON_RPC_RS, connection_id: str) -> bool:
        callback = self._callbacksOnClientRS.get(rs.id, None)
        if callback is not None:
            await callback(rs, connection_id)
            self._callbacksOnClientRS.pop(rs.id)
        else:
            self.logger.debug(f'Hending RS without callback. {rs=}, {connection_id=}')
        return True

    async def _sendRQ_GET_TIME(self, connection_id: str):
        self.logger.info(f'_sendRQ_GET_TIME {Utils.getCurrentTsMs()=}')
        rq = JSON_RPC_RQ(
            method=MetronomeServerMethod.GET_TIME,
            params=None,
            id=Utils.getNextId(),
        )
        await self._sendRQToClient(rq=rq, connection_id=connection_id, callbackOnRS=self._parseRS_GET_TIME)

    async def _parseRS_GET_TIME(self, rs: JSON_RPC_RS, connection_id: str):
        self.logger.info(f'{Utils.getCurrentTsMs()=}')
        currentTsMs: int = Utils.getCurrentTsMs()
        startRQTsMs: int = self._calcDifferenceInTsMs.get(connection_id, 0)
        clientTsMs: int = rs.result.get("ts_ms", 0)
        differenceInTsMs: int = int(currentTsMs - ((currentTsMs - startRQTsMs) / 2) - clientTsMs)
        user = await self.store.usersAccessor.getUser(connection_id)
        # if user.client_id == 1:
            # self.logger.info(f'differenceInTsMs += 50 {self.store.usersAccessor.getDifferenceInTsMs(connection_id)=}')
            # differenceInTsMs += 50
        await self.store.usersAccessor.setDifferenceInTsMs(connection_id=connection_id, differenceInTsMs=differenceInTsMs)

    async def _sendTestDataRS(self, connection_id: str):
        rs = JSON_RPC_RS(
            result={
                "timestamp": f"{datetime.now().timestamp()}"
                , "date1 from python timestamp": f"{datetime.utcfromtimestamp(datetime.now().timestamp())}"
                , "date2 from int timestamp": f"{datetime.utcfromtimestamp(round(datetime.now().timestamp() * 1000) / 1e3)}"
            },
            id=None,
        )
        await self.store.wsAccessor.pushData(rs, connection_id=connection_id)

    async def _sendRQToClient(self, rq: JSON_RPC_RQ, connection_id: str, callbackOnRS: typing.Callable[[str], typing.Awaitable]):
        self._callbacksOnClientRS[rq.id] = callbackOnRS
        await self.store.wsAccessor.pushData(data=rq, connection_id=connection_id)

    async def onUserDisconnect(self, connection_id: str) -> None:
        user = await self.store.usersAccessor.getUser(connection_id)
        if user is not None:
            await self.store.groupAccessor.removeUserFromAllGroups(user)
            await self.store.usersAccessor.removeUser(connection_id)

