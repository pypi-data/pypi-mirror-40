import sys
import socket
import pickle
import salaga.clusterOp
import salaga.utils.slgcodes as scd
import salaga.utils.localMan as lm
import salaga.utils.hashCodeGen as hcg
import salaga.utils.neighbour as neigh

version = '0.0.1a3'


def get(key, remote=True):
    """
    INPUT  : key.
    OUTPUT : value corresponding to that key.
    """
    if(remote):
        try:
            ip = key.split('-')[0]
            port = int(scd.SLGDPORT)
            BUFFER_SIZE = scd.SLGDBUFFSZ
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client.connect((ip, port))
            client.send(pickle.dumps(('g', key)))
            data = client.recv(BUFFER_SIZE)
            client.close()
            return(pickle.loads(data))

        except Exception as e:
            print(str(e))
            return(None)

    else:
        ret = lm.retrieve(key)
        return(ret)


def put(data, remote=False):
    """
    INPUT  : data to be stored.
    OUTPUT : A Non-negative key number if
             successful, negative number on
             failure.
    """
    if(not remote):
        myIP = scd.myIP
        key = hcg.newStore(myIP)
        ret = lm.store(key, data)
        if(ret is not None):
            return(key)
        return(scd.FAILURE.codeNum)
    else:
        try:
            ip = neigh.getNeighbour()
            port = int(scd.SLGDPORT)
            BUFFER_SIZE = scd.SLGDBUFFSZ
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            client.connect((ip, port))
            client.send(pickle.dumps(('p', data)))
            key = client.recv(BUFFER_SIZE)
            client.close()
            return(pickle.loads(key))
        except Exception as e:
            print(str(e))


def printUsage():
    print("Usage : python3 salaga.py {-p | -g} filename")
