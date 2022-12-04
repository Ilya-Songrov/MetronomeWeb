import argparse
from dataclasses import dataclass, field


@dataclass
class Arguments:
    listen_host: str        = 'localhost'
    listen_port: int        = 8080
    connect_host: str       = None
    connect_port: int       = None

    def __str__(self):
        return (f"Arguments("
            f" {self.listen_host=}"
            f", {self.listen_port=}"
            f", {self.connect_host=}"
            f", {self.connect_port=}"
            ")"
        )


class MyArgumentParser:
    def __init__(self):
        pass

    def parseArguments() -> 'Arguments':
        parser = argparse.ArgumentParser(description="My description")
        parser.add_argument("--listen_host", type=str, required=True,
                            help="""Listening server host """)
        parser.add_argument("--listen_port", type=int, required=True,
                            help="""Listening server port """)
        parser.add_argument("--connect_host", type=str, required=False,
                            help="""Connect host for client """)
        parser.add_argument("--connect_port", type=int, required=False,
                            help="""Connect port for client """)

        parserArgs = parser.parse_args()
        if parserArgs == None:
          raise Exception("Can't parse input parameters")

        appArgs = Arguments()
        appArgs.listen_host     = parserArgs.listen_host
        appArgs.listen_port     = parserArgs.listen_port
        appArgs.connect_host    = parserArgs.listen_host
        appArgs.connect_port    = parserArgs.listen_port
        if parserArgs.connect_host is not None:
            appArgs.connect_host        = parserArgs.connect_host
        if parserArgs.connect_port is not None:
            appArgs.connect_port        = parserArgs.connect_port

        return appArgs

