import typing

from App.Store.Metronome.MetronomeManager import MetronomeManager
from App.Store.Users.UsersAccessor import UsersAccessor
from App.Store.Groups.GroupsAccessor import GroupsAccessor
from App.Store.WS.WSAccessor import WSAccessor

if typing.TYPE_CHECKING:
    from App.Base.Application import Application


class Store:
    def __init__(self, app: "Application"):
        self.app = app
        self.metronomeManager   = MetronomeManager(self)
        self.wsAccessor         = WSAccessor(self)
        self.usersAccessor      = UsersAccessor(self)
        self.groupAccessor      = GroupsAccessor(self)
