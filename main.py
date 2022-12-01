import logging
from logging import getLogger

from aiohttp import web

from App.Base.Application import Application
from App.Core.Routes import setupRoutes
from App.Store.Store import Store


def createApp() -> Application:
    app = web.Application()
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s %(levelname)s] {%(pathname)s:%(lineno)d} [p%(process)s]: %(message)s')
    app.logger = getLogger()
    app.store = Store(app)
    setupRoutes(app)
    return app


if __name__ == '__main__':
    web.run_app(createApp(), host='192.168.0.106', port=8000)
