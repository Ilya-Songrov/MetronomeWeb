import os
import argparse
from dataclasses import dataclass, field
from Utils.AppArguments import AppArguments



class MyArgumentParser:
    def __init__(self):
        pass

    def parseArguments() -> 'AppArguments':
        parser = argparse.ArgumentParser(description="My description")
        parser.add_argument('-v', '--version', action='version', version='1.0.0')
        parser.add_argument("--listen_host", type=str, required=True,
                            help="""Listening server host """)
        parser.add_argument("--listen_port", type=int, required=True,
                            help="""Listening server port """)
        parser.add_argument("--log_dir_to_save", type=str, required=False,
                            help="""Directory to save logs""")

        parserArgs = parser.parse_args()
        if parserArgs == None:
          raise Exception("Can't parse input parameters")

        appArgs = AppArguments()
        appArgs.listen_host         = parserArgs.listen_host
        appArgs.listen_port         = parserArgs.listen_port
        if parserArgs.log_dir_to_save:
          appArgs.log_dir_to_save     = os.path.abspath(parserArgs.log_dir_to_save)
        print(f"{appArgs=}")
        return appArgs

