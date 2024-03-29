import asyncio
import json
import typing
import uuid
from asyncio import Task, CancelledError
from dataclasses import dataclass, asdict

from aiohttp.web_ws import WebSocketResponse

from App.Store.jsonrpc.jsonrpc import JSON_RPC_BASE, JSON_RPC_RQ, JSON_RPC_RS
from App.Base.Accessor import BaseAccessor
from App.Base.Utils import doByTimeoutWrapper

if typing.TYPE_CHECKING:
    from App.Base.Application import Request



class WSContext:
    def __init__(
            self,
            accessor: 'WSAccessor',
            request: 'Request',
            close_callback: typing.Callable[[str], typing.Awaitable] | None = None,
    ):
        self._accessor = accessor
        self._request = request
        self.connection_id: typing.Optional[str] = None
        self._close_callback = close_callback

    async def __aenter__(self) -> str:
        self.connection_id = await self._accessor.open(self._request, closeCallback=self._close_callback)
        return self.connection_id

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._accessor.close(self.connection_id)


@dataclass
class Connection:
    session: WebSocketResponse
    timeoutTask: Task
    closeCallback: typing.Callable[[str], typing.Awaitable] | None


class WSAccessor(BaseAccessor):
    class Meta:
        name = 'ws_accessor'

    CONNECTION_TIMEOUT_SECONDS = 12315

    def _init_(self) -> None:
        self._connections: dict[str, Connection] = {}

    async def open(
            self,
            request: 'Request',
            closeCallback: typing.Callable[[str], typing.Awaitable[typing.Any]] | None = None,
    ) -> str:
        ws_response = WebSocketResponse()
        await ws_response.prepare(request)
        connection_id = str(uuid.uuid4())

        self.logger.info(f'Handling new connection. Host: {request.host} '
                f'Generate ID for it: {connection_id=}')

        self._connections[connection_id] = Connection(
            session=ws_response,
            timeoutTask=self._createTimeoutTask(connection_id),
            closeCallback=closeCallback,
        )
        return connection_id

    def _createTimeoutTask(self, connection_id: str) -> Task:
        def logTimeout(result: Task):
            try:
                exc = result.exception()
            except CancelledError:
                return

            if exc:
                self.logger.error('Can not close connection by timeout', exc_info=result.exception())
            else:
                self.logger.info(f'Connection with {connection_id=} was closed by inactivity')

        task = asyncio.create_task(
            doByTimeoutWrapper(
                self.close,
                self.CONNECTION_TIMEOUT_SECONDS,
                args=[connection_id],
            )
        )
        task.add_done_callback(logTimeout)
        return task

    async def close(self, connection_id: str):
        connection = self._connections.pop(connection_id, None)
        if not connection:
            return

        self.logger.info(f'Closing {connection_id=}')

        if connection.closeCallback:
            await connection.closeCallback(connection_id)

        if not connection.session.closed:
            await connection.session.close()

    async def pushData(self, data: JSON_RPC_BASE, connection_id: str):
        self.logger.info(f'Push {data=} to {connection_id=}')
        data = json.dumps(asdict(data), separators=(',', ':'))
        return await self._pushData(self._connections[connection_id].session, data=data)

    async def _pushData(self, connection: 'WebSocketResponse', data: str):
        await connection.send_str(data)

    async def broadcast(self, id_data: list[tuple[JSON_RPC_BASE,str]]):
        self.logger.info(f'Broadcasting {id_data=}')
        ops = []
        for tupIdData in id_data:
            ops.append(self.pushData(data=tupIdData[0], connection_id=tupIdData[1]))
        await asyncio.gather(*ops)

    async def streamData(self, connection_id: str) -> typing.AsyncIterable[JSON_RPC_BASE]:
        async for message in self._connections[connection_id].session:
            await self.refreshConnection(connection_id)
            self.logger.info(f"Input {message=}")
            data: json = message.json()  # noqa
            if 'method' in data:
                yield JSON_RPC_RQ(method=data['method'], params=data['params'], id=data['id'], jsonrpc=data['jsonrpc'])
            else:
                yield JSON_RPC_RS(result=data['result'], id=data['id'], jsonrpc=data['jsonrpc'])

    async def refreshConnection(self, connection_id: str):
        self._connections[connection_id].timeoutTask.cancel()
        self._connections[connection_id].timeoutTask = self._createTimeoutTask(connection_id)
