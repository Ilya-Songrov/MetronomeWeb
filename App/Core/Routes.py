import os

from aiohttp.abc import Application

from App import BASE_DIR
from App.Core.Views import IndexView, WSConnectView, IndexViewIcon


def setupRoutes(app: Application):
    app.router.add_view("/connect", WSConnectView)
    app.router.add_view("/", IndexView)
    app.router.add_static("/static", os.path.join(BASE_DIR, "client", "static"), follow_symlinks=True)
    # app.router.add_view("/favicon.ico", IndexViewIcon)
