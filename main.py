import os
import logging
from logging import getLogger

from aiohttp import web

from Utils.ArgumentParser import MyArgumentParser, Arguments
from Utils.Utils import Utils
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
    appArgs = MyArgumentParser.parseArguments()
    Utils.replaceStrInFile({"${METRONOME_SERVER_CONNECT_HOST}": appArgs.connect_host
            , "${METRONOME_SERVER_CONNECT_PORT}": str(appArgs.connect_port)}, f"{os.path.dirname(__file__)}/client/static/js/network.js")
    web.run_app(createApp(), host=appArgs.listen_host, port=appArgs.listen_port)
