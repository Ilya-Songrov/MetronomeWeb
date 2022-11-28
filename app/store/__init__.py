import typing

from app.store.geo.geo_manager import GeoManager
from app.store.users.users_accessor import UsersAccessor
from app.store.Groups.GroupsAccessor import GroupsAccessor
from app.store.ws.ws_accessor import WSAccessor

if typing.TYPE_CHECKING:
    from app.base.application import Application


class Store:
    def __init__(self, app: "Application"):
        self.app = app
        self.wsAccessor     = WSAccessor(self)
        self.geoManager     = GeoManager(self)
        self.usersAccessor  = UsersAccessor(self)
        self.groupAccessor  = GroupsAccessor(self)
