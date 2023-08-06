import os
import socket


def printCode(CODE):
    print("SALAGA encountered an error with code: {} ({})".
          format(CODE.codeNum, CODE.codeMsg))


class CODES:
    def __init__(self, codeNum, codeMsg):
        self.codeNum = codeNum
        self.codeMsg = codeMsg


tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tmp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tmp.connect(('254.255.255.255', 80))
myIP = tmp.getsockname()[0]
tmp.close()

SLGHOME = os.environ.get('SLGHOME')
SLGCONF = os.environ.get('SLGCONF')

SLGDIP = '0.0.0.0'
SLGDPORT = '7777'
SLGCPORT = '7776'
SLGDBUFFSZ = 10240

FAILURE = CODES(-1, "FAILURE")
SUCCESS = CODES(0, "SUCCESS")

NOHOME = CODES(1, "$SLGHOME not set")
IPFAIL = CODES(2, "IPv4 not assigned to machine")
NOENT = CODES(3, "No entry found")
NOWPEM = CODES(4, "Write permissions denied in $SLGHOME = {}".format(SLGHOME))
NORPEM = CODES(5, "Read permissions denied in $SLGHOME = {}".format(SLGHOME))
NOCONF = CODES(6, "$SLGCONF not set")

if(SLGHOME is None):
    printCode(NOHOME)
    exit(NOHOME.codeNum)

if(SLGCONF is None):
    printCode(NOCONF)
    exit(NOCONF.codeNum)

if(myIP is None):
    printCode(IPFAIL)
    exit(IPFAIL.codeNum)
