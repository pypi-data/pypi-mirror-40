import pickle

# The 2 main functions provided by mail man to the upper layers


def feed(socketObj, obj):
    """
    Socket send() wrapper
    """
    serializedObj = pickle.dumps(obj)
    socketObj.send(serializedObj)


def eat(socketObj, size=1024):
    """
    Socket recv() wrapper
    """
    return(pickle.loads(socketObj.recv(size)))
