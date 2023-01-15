import time
from aiohttp import web
from Utils.ArgumentParser import MyArgumentParser, AppArguments
from Utils.MyLogger import MyLogger
from App.Base.Application import Application
from App.Core.Routes import setupRoutes
from App.Store.Store import Store


def createApp() -> Application:
    app         = web.Application()
    app.store   = Store(app)
    setupRoutes(app)
    return app

if __name__ == '__main__':
    logger                          = MyLogger.createLoggerConfigsStdout()
    appArgs                         = AppArguments()

    while True:
        try:
            appArgs         = MyArgumentParser.parseArguments()
            logger          = MyLogger.createLoggerConfigs(appArgs.log_dir_to_save, "metronome-web")
            web.run_app(createApp(), host=appArgs.listen_host, port=appArgs.listen_port)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt exception was caught")
            break
        except Exception as ex:
            logger.exception(ex)

        logger.info(f"Sleep. Next attempt will be in 10000 milliseconds.\n\n")
        time.sleep(10)
    