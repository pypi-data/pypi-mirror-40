import os


def printCode(CODE):
    print("SALAGA encountered an error with code: {} ({})".
          format(CODE.codeNum, CODE.codeMsg))


class CODES:
    def __init__(self, codeNum, codeMsg):
        self.codeNum = codeNum
        self.codeMsg = codeMsg


SLGHOME = os.environ.get('SLGHOME')

FAILURE = CODES(-1, "FAILURE")
SUCCESS = CODES(0, "SUCCESS")

NOHOME = CODES(1, "$SLGHOME not set")
NOENT = CODES(2, "No entry found")
NOWPEM = CODES(3, "Write permissions denied in $SLGHOME = {}".format(SLGHOME))
NORPEM = CODES(3, "Read permissions denied in $SLGHOME = {}".format(SLGHOME))
