#!/usr/bin/python3

import asyncio
import websockets
import inspect
from threading import Timer

# ----------- Colored output -----------
class bcolors:
    HEADER      = '\033[95m'
    OKBLUE      = '\033[94m'
    OKCYAN      = '\033[96m'
    OKGREEN     = '\033[92m'
    RED         = '\033[31m'
    MAGENTA     = '\033[35m'
    WARNING     = '\033[93m'
    FAIL        = '\033[91m'
    ENDC        = '\033[0m'
    BOLD        = '\033[1m'
    UNDERLINE   = '\033[4m'
    
def print_c(col, str):
    """Outputs to the terminal a string (str) of the specified color (col)"""
    print("{}{}{}".format(col, str, bcolors.ENDC))
def print_c_prefix_str(col, prefix, str):
    """Outputs to the terminal a string (str) of the specified color (col)"""
    print("{}{}{}{}".format(col, prefix, bcolors.ENDC, str))
# ----------- Colored output -----------

listClients = set()

async def sendCustomData():
    print("print_line: ", inspect.currentframe())
    await asyncio.sleep(4)
    print("print_line: ", inspect.currentframe())
    for client in listClients:
        await client.send("custom data")

async def handler(websocket, path):
    listClients.add(websocket)
    print("listClients:", listClients)
    while True:
        try:
            message = await websocket.recv()
#        finally:
            # Unregister.
#            listClients.remove(websocket)
        except websockets.ConnectionClosedOK:
            listClients.remove(websocket)
            print(f"Disconnected:", websocket.id)
            print(f"local_address:", websocket.local_address)
            print(f"remote_address:", websocket.remote_address)
            break
        reply = f"Data recieved as:  {message}"
        print(f"Input message: {message}")
        print(f"id:", websocket.id)
        print(f"local_address:", websocket.local_address)
        print(f"remote_address:", websocket.remote_address)
        await websocket.send(reply)

async def startServer():
#    async with websockets.serve(handler, "0.0.0.0", 8001):
#        await asyncio.Future()  # run forever
    await websockets.serve(handler, "0.0.0.0", 8001)
    my_future = await asyncio.Future()
    print(my_future.done())

async def main():
    await asyncio.gather(sendCustomData(), startServer())


if __name__ == "__main__":
#    print("Server started http://%s:%s" % (hostName, serverPort))
    print("Server started")
    try:

#        timer = loop.call_later(timeout, lambda: asyncio.ensure_future(some_job()))
#        timer = loop.call_later(2, lambda: asyncio.ensure_future(sendCustomData()))

#        t = Timer(4.0, sendCustomData())
#        t.start() # after 30 seconds, "hello, world" will be printed

#        print("print_line: ", inspect.currentframe())
        asyncio.run(main())
        print("print_line: ", inspect.currentframe())

#        start_server = websockets.serve(handler, "", 8001)
#        asyncio.get_event_loop().run_until_complete(start_server)
#        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass

    print("Server stopped.")
