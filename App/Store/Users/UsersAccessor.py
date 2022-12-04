from dataclasses import dataclass, asdict
from Utils.Utils import Utils

from App.Base.Accessor import BaseAccessor


@dataclass
class User:
    connection_id: str      = ""
    client_id: int          = -1
    differenceInTsMs: int   = 0

    def __str__(self):
        return f'User<{self.connection_id=},{self.client_id=},{self.name=},{self.differenceInTsMs=}>'


class UsersAccessor(BaseAccessor):
    def _init_(self) -> None:
        self._users: dict[str, User] = {}
        self._client_ids: list[int] = list(range(9999, 0, -1))

    async def list_users(self) -> list[User]:
        return list(self._users.values())

    async def addUser(self, connection_id: str) -> User:
        user = await self.getUser(connection_id)
        if user is None:
            user = User(connection_id=connection_id,client_id= await self._getFreeClientId())
            self.logger.debug(f'Add new {user=}')
            self._users[connection_id] = user
        return user

    async def removeUser(self, connection_id: str) -> None:
        user = await self.getUser(connection_id)
        if user is not None:
            self.logger.debug(f'Remove {user=}')
            self._client_ids.append(user.client_id)
            self._users.pop(connection_id)

    async def getUser(self, connection_id: str) -> User | None:
        return self._users.get(connection_id, None)
    
    async def setDifferenceInTsMs(self, connection_id: str, differenceInTsMs: int) -> None:
        user = await self.getUser(connection_id)
        if user is not None:
            user.differenceInTsMs = differenceInTsMs
            self.logger.debug(f'Set differenceInTsMs {user=}')
    
    async def getDifferenceInTsMs(self, connection_id: str) -> int:
        user = await self.getUser(connection_id)
        if user is not None:
            self.logger.debug(f'Get differenceInTsMs {user=}')
            return user.differenceInTsMs
        return 0

    async def _getFreeClientId(self) -> int:
        try:
            return self._client_ids.pop()
        except:
            return Utils.getCurrentTimestampMs()
