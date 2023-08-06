import os
import pickle
import salaga.utils.slgcodes as scd

# The 2 main functions provided by local man to the upper layers


def store(key, data):
    retCode = checkDir()
    if(retCode != scd.SUCCESS):
        scd.printCode(retCode)
        return(None)
    try:
        slghomefd = open(scd.SLGHOME+"/"+key+".salg", 'wb')
    except FileNotFoundError:
        scd.printCode(scd.NOENT)
        return(None)
    pickle.dump(data, slghomefd)
    slghomefd.close()
    return(scd.SUCCESS)


def retrieve(key):
    retCode = checkDir()
    if(retCode != scd.SUCCESS):
        scd.printCode(retCode)
        return(None)
    try:
        slghomefd = open(scd.SLGHOME+"/"+key+".salg", 'rb')
    except FileNotFoundError:
        scd.printCode(scd.NOENT)
        return(None)
    data = pickle.load(slghomefd)
    slghomefd.close()
    return(data)

# sub-Utility functions used by the above
# functions


def checkDir():
    if(os.environ.get('SLGHOME') is None):
        return(scd.NOHOME)
    if(not os.access(scd.SLGHOME, os.W_OK)):
        return(scd.NOWPEM)
    if(not os.access(scd.SLGHOME, os.R_OK)):
        return(scd.NORPEM)
    return(scd.SUCCESS)
