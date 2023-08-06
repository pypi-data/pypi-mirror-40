import socket
import pickle
import salaga as slg
from threading import Thread
import salaga.utils.slgcodes as scd


def slgDaemon():
    BUFFER_SIZE = scd.SLGDBUFFSZ

    slgd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    slgd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    slgd.bind((scd.SLGDIP, int(scd.SLGDPORT)))
    slgdChildren = []

    class _SLGDCHILD(Thread):

        def __init__(self, connection, clientIP, port):
            Thread.__init__(self)
            self.clientIP = clientIP
            self.port = port
            self.connection = connection

        def run(self):
            data = pickle.loads(self.connection.recv(BUFFER_SIZE))
            if(data[0] == 'p'):
                key = slg.put(data[1], False)
                connection.send(pickle.dumps(key))
            elif(data[0] == 'g'):
                key = data[1]
                data = slg.get(key, False)
                if(data is not None):
                    connection.send(pickle.dumps(data))
                else:
                    connection.send("No data".encode())

    while(True):
        try:
            slgd.listen(5)
            (connection, (ip, port)) = slgd.accept()
            slgdChild = _SLGDCHILD(connection, ip, port)
            slgdChild.start()
            slgdChildren.append(slgdChild)
        except Exception as e:
            print(str(e))
            slgd.close()
            break

    for child in slgdChildren:
        child.join()


# For testing purposes

if(__name__ == "__main__"):
    slgDaemon()
