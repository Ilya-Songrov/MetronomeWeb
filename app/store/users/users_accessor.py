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

    async def update_coords(
            self,
            connection_id: str,
    ):
        pass

    async def add(
            self,
            connection_id: str,
            name: str,
    ) -> User:
        user = await self.get(connection_id)
        if user is not None:
            return user
        user = User(
            client_id= await self._get_free_client_id(),
            name=name,
        )
        self._users[connection_id] = user
        return user

    async def remove(self, connection_id: str) -> None:
        user = await self.get(connection_id)
        self._client_ids.append(user.client_id)
        self._users.pop(connection_id)

    async def get(self, connection_id: str) -> User | None:
        return self._users.get(connection_id, None)
    
    async def _get_free_client_id(self) -> int:
        try:
            return self._client_ids.pop()
        except:
            return Utils.getCurrentTimestampMs()
