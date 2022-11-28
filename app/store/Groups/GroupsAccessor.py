from dataclasses import dataclass, field
from utils.Utils import Utils

from app.base.accessor import BaseAccessor
from app.store.users.users_accessor import User

@dataclass
class Group:
    userOwner: 'User'
    subscribedUsers: list['User'] = field(default_factory=list)

    def __str__(self):
        return f'Group<{self.userOwner=},{self.subscribedUsers=}>'


class GroupsAccessor(BaseAccessor):
    def _init_(self) -> None:
        self._groups: dict[int, Group] = {}

    async def listGroups(self) -> list[Group]:
        return list(self._groups.values())

    async def createGroup(self, userOwner: 'User') -> Group:
        group = await self.getGroup(userOwner.client_id)
        if group is None:
            group = Group(userOwner=userOwner)
            self.logger.info(f'Create new {group=}')
            self._groups[userOwner.client_id] = group
        return group
    
    async def addUserToGroup(self, user: 'User', group_id: int):
        group = await self.getGroup(group_id)
        if group is not None and user not in group.subscribedUsers:
            self.logger.info(f'Add {user=} to {group=}')
            group.subscribedUsers.append(user)

    async def removeUserFromGroup(self, user: 'User', group_id: int):
        group = await self.getGroup(group_id)
        if group is not None and user in group.subscribedUsers:
            self.logger.info(f'Remove {user=} from {group=}')
            group.subscribedUsers.remove(user)

    async def removeGroup(self, group_id: int) -> None:
        self._groups.pop(group_id)

    async def getGroup(self, group_id: int) -> Group | None:
        return self._groups.get(group_id, None)
    
