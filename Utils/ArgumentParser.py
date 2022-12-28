import argparse
from dataclasses import dataclass, field


@dataclass
class Arguments:
    listen_host: str        = 'localhost'
    listen_port: int        = 8080

    def __str__(self):
        return (f"Arguments("
            f" {self.listen_host=}"
            f", {self.listen_port=}"
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

        parserArgs = parser.parse_args()
        if parserArgs == None:
          raise Exception("Can't parse input parameters")

        appArgs = Arguments()
        appArgs.listen_host     = parserArgs.listen_host
        appArgs.listen_port     = parserArgs.listen_port
        return appArgs

