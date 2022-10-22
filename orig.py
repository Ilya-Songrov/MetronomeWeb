#!/usr/bin/python3

import json
import time
import ssl
import pprint
import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client, urllib.parse


hostName = "10.255.249.140"
serverPort = 7070

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

class MyServer(BaseHTTPRequestHandler):
#    def do_GET(self):
#        self.send_response(200)

    def do_POST(self):
        rqMethod    = self.headers.get('X-FXAPI-RQ-METHOD')
        rqBody      = self.getRQBody()
        print_c_prefix_str(bcolors.OKCYAN, "rqHeaders: ", "\n" + str(self.headers).rstrip())
        print_c_prefix_str(bcolors.OKCYAN, "rqMethod: ", rqMethod)
        print_c_prefix_str(bcolors.OKCYAN, "rqBody: ", rqBody)
        rsCode      = -1
        rsHeaders   = {}
        rsBody      = bytes("", "utf-8")
        if self.isTestUserOne(rqBody):
            rqValue     = self.headers.get('X-FXAPI-VALUE', "")
            rsBody      = self.getCustomBody(rqMethod, rqValue)
            rsHeaders   = self.getCustomHeaders(rsBody)
            rsCode      = 200
        elif self.isTestUserTwo(rqBody):
            rsCode, rsHeaders, rsBody = self.getRedirectResponse(rqBody, "10.255.249.140", 8080, "/processing_api140/testpc/")
        else:
            rsCode, rsHeaders, rsBody = self.getRedirectResponse(rqBody, "10.255.249.140", 8080, "/processing_api140/testpc/")

        self.sendPOSTResponse(rsCode, rsHeaders, rsBody)
        print_c_prefix_str(bcolors.OKBLUE, "rsCode: ", rsCode)
        print_c_prefix_str(bcolors.OKBLUE, "rsHeaders: ", "\n" + str(rsHeaders).rstrip())
        print_c_prefix_str(bcolors.OKBLUE, "rsBody: ", self.modifyBody(rsBody))
        print("\n\n")

    def sendPOSTResponse(self, rsCode, rsHeaders, rsBody):
        self.send_response(rsCode)
        for h in rsHeaders:
            self.send_header(h, rsHeaders[h])
        self.end_headers()
        self.wfile.write(rsBody)

    def getRedirectResponse(self, rqBody, redirectHostName, redirectServerPort, redirectRout):
        print("Redirect to:", redirectHostName + ":" + str(redirectServerPort) + redirectRout)
        connection = http.client.HTTPConnection(redirectHostName, port=redirectServerPort)
        connection.request('POST', redirectRout, rqBody, self.headers)
        response = connection.getresponse()
        rsBody = response.read()
        connection.close()
        return response.code, response.headers, rsBody

    def getRQBody(self):
        content_len = int(self.headers.get('Content-Length'))
        if content_len:
            return self.rfile.read(content_len)

    def isJson(self, myjson):
        try:
            json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def modifyBody(self, body):
        if self.isJson(body):
            return json.dumps(json.loads(body), ensure_ascii=False, indent=4)
        else:
            return body.decode('UTF-8')

    def isTestUserOne(self, rqBody):
        return False;

        if str(rqBody).find("380983008644") != -1:
            return True;
        elif str(rqBody).find("13741ac949e67082e19976a30667bd07") != -1: # uuid of 380983008644
            return True;
        elif str(rqBody).find("bbf05e9b25d7e27d3a7715296158e2ed") != -1: # "login":"3139","passwordHash":"bbf05e9b25d7e27d3a7715296158e2ed"
            return True;
        return False;

    def isTestUserTwo(self, rqBody):
        if str(rqBody).find("380983008644") != -1:
            return True;
        elif str(rqBody).find("13741ac949e67082e19976a30667bd07") != -1: # uuid of 380983008644
            return True;
        return False;

    def getCustomHeaders(self, rsBody):
        headers = {}
        headers["Connection"] = "close"
        headers["X-FXAPI-RES-CODE"] = "OK"
        headers["X-FXAPI-RES-MSG"] = "Success"
        headers["Content-Length"] = str(len(rsBody))
        return headers

    def getCustomBody(self, rqMethod, rqValue):
        body = bytes("{}", "utf-8")
        if rqMethod == "crm.operator.Search" and len(rqValue) == 0:
            body = bytes("""
            {
              "uid": "13741ac949e67082e19976a30667bd07",
              "buyer": {
                "uid": "13741ac949e67082e19976a30667bd07",
                "firstName": "Илья",
                "lastName": "",
                "middleName": "",
                "birthDate": "0000-00-00",
                "cellphone": "380983008644",
                "email": null,
                "cardNum": "5000098033336"
              },
              "res": 1,
              "requestId": "01090b13d28d8adce47ebf0a87e4f510-evarush-6225f551e1078"
            }
            """, "utf-8")
        elif rqMethod == "crm.operator.Search" and rqValue == "26":
            body = bytes("""
            {
              "res": 26,
              "requestId": "efb88c21-b1dc-30b3-d2be-662df76989a0",
              "error": "клиент не найден"
            }
            """, "utf-8")
        elif rqMethod == "crm.cabinet.Register":
            body = bytes("""
            {
              "uid": "148d84f8961a0999dcc8b34814fadd06",
              "res": 1,
              "requestId": "9847ea011e3a98374158961b2220a022-evarush-6223d0785d014"
            }
            """, "utf-8")
        elif rqMethod == "core.user.Login":
            body = bytes("""
            {
              "sid": "c78918a3011d1d40191c3beef3be56bc",
              "role": null,
              "permissions": 0,
              "res": 1,
              "requestId": "94393b901f9e16c7fd407ba62bbb125f-evarush-6230468f27472"
            }
            """, "utf-8")
        elif rqMethod == "crm.cabinet.Info":
            body = bytes("""
            {
                "res": 1,
                "requestId": "43938488-5abf-78b1-5068-678254c96af5",
                "error": "",
                "cards": [
                    {
                        "cardNum": "5000098033336",
                        "state": "3",
                        "cardStatus": ""
                    }
                ],
                "balances": [
                    {
                        "balanceTypeId": "0",
                        "balanceTypeName": "",
                        "balance": 0,
                        "inactiveBalance": 0
                    }
                ],
                "buyer": {
                    "email": "",
                    "firstName": "",
                    "middleName": "",
                    "lastName": "",
                    "sex": "2",
                    "birthDate": "1970-01-01",
                    "addrZIP": "",
                    "addrRegion": "",
                    "addrCity": "",
                    "addrStreet": "",
                    "addrBuilding": "",
                    "addrHousing": "",
                    "addrFlat": "",
                    "sendSMS": "1",
                    "sendEmail": "",
                    "preferredContact": "0",
                    "printName": "",
                    "keyword": "",
                    "phoneConfirmed": "0",
                    "emailConfirmed": "0",
                    "registrationDate": "",
                    "lastAuthDate": "1970-01-01",
                    "cellphone": "",
                    "cards": "5000098033336",
                    "buyerStatus": "",
                    "spendAllowed": "0",
                    "oddMoneyBalance": "0",
                    "oddMoneyFlags": "0",
                    "buyerId": "3100000178",
                    "subscriptions": []
                }
            }
            """, "utf-8")
        elif rqMethod == "crm.buyer.getAuthToken":
            body = bytes('{"res":1,"requestId":"bf4a3eb4-e50d-96ad-1e2f-65dfb281cd2c","error":"","authToken":"0031944277632"}', "utf-8")
#            body = bytes('{"res":41,"error":"Размер префикса должен быть 0","requestId":"7c06e2dae3a599c533ff4ba32655b1ee-evarush-62284ea0befeb"}', "utf-8")
        return body;


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

