from dataclasses import dataclass, asdict
from utils.Utils import Utils

from app.base.accessor import BaseAccessor


@dataclass
class User:
    client_id: int
    name: str

    def __str__(self):
        return f'User<{self.client_id=},{self.name=}>'


class UsersAccessor(BaseAccessor):
    def _init_(self) -> None:
        self._users: dict[str, User] = {}
        self._client_ids: list[int] = list(range(9999, 0, -1))

    async def list_users(self) -> list[User]:
        return list(self._users.values())

    async def addUser(self, connection_id: str, name: str) -> User:
        user = await self.getUser(connection_id)
        if user is None:
            user = User(client_id= await self._getFreeClientId(),name=name)
            self.logger.info(f'Add new {user=}')
            self._users[connection_id] = user
        return user

    async def removeUser(self, connection_id: str) -> None:
        user = await self.getUser(connection_id)
        if user is not None:
            self.logger.info(f'Remove {user=}')
            self._client_ids.append(user.client_id)
            self._users.pop(connection_id)

    async def getUser(self, connection_id: str) -> User | None:
        return self._users.get(connection_id, None)
    
    async def _getFreeClientId(self) -> int:
        try:
            return self._client_ids.pop()
        except:
            return Utils.getCurrentTimestampMs()
