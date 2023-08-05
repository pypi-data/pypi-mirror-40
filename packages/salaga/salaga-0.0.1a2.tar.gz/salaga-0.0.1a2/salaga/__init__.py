import sys
import socket
import salaga.clusterOp
import salaga.utils.slgcodes as scd
import salaga.utils.localMan as lm
import salaga.utils.hashCodeGen as hcg

version = '0.0.1a2'


def get(key):
    """
    INPUT  : key.
    OUTPUT : value corresponding to that key.
    """
    ret = lm.retrieve(key)
    return(ret)


def put(value):
    """
    INPUT  : value to be stored.
    OUTPUT : A Non-negative key number if
             successful, negative number on
             failure.
    """
    key = hcg.newStore()
    ret = lm.store(key, value)
    if(ret is not None):
        return(key)
    return(scd.FAILURE.codeNum)


if(__name__ == "__main__"):
    if(len(sys.argv) >= 3):
        if((sys.argv[1] == '-s') or (sys.argv[1] == '--store')):
            fd = open(sys.argv[2], "rb")
            key = put(fd.read())
            print("file : {} has been stored in Salaga\n Access Key is : {}".
                  format(sys.argv[2], key))
        elif((sys.argv[1] == '-g') or (sys.argv[1] == '--get')):
            ofd = open("OUTPUT.salg", "wb")
            data = get(int(sys.argv[2]))
            ofd.write(data)
    else:
        printUsage()


def printUsage():
    print("Usage : python3 salaga.py {-s | -g} filename")
