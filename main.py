import logging
from logging import getLogger

from aiohttp import web

from app.base.application import Application
from app.core.routes import setup_routes
from app.store import Store


def create_app() -> Application:
    app = web.Application()
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s %(levelname)s] {%(pathname)s:%(lineno)d} [p%(process)s]: %(message)s')
    app.logger = getLogger()
    app.store = Store(app)
    setup_routes(app)
    return app


if __name__ == '__main__':
    print("test1")
    web.run_app(create_app(), host='192.168.0.106', port=8000)
    print("test2")
