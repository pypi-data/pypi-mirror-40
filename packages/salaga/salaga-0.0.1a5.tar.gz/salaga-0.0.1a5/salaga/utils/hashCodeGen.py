import os
import sys
import salaga.utils.slgcodes as scd


def newStore(ip):
    try:
        seqfd = open(scd.SLGHOME+"/tmp/SEQ.salgtmp", "r")
    except Exception as e:
        initSEQ()
    finally:
        seqfd = open(scd.SLGHOME+"/tmp/SEQ.salgtmp", "r")
        nextseq = seqfd.read()
        if(nextseq is None):
            initSEQ()
        seqfd.close()
        seqfd = open(scd.SLGHOME+"/tmp/SEQ.salgtmp", "w")
        seqfd.write(str(int(nextseq)+1))
        seqfd.close()
        return(ip + '-' + str(hash(nextseq) + sys.maxsize))


def initSEQ():
    if(not os.path.isdir(scd.SLGHOME)):
        os.mkdir(scd.SLGHOME)
    if(not os.path.isdir(scd.SLGHOME+"/tmp")):
        os.mkdir(scd.SLGHOME+"/tmp")
    seqfd = open(scd.SLGHOME+"/tmp/SEQ.salgtmp", "w")
    seqfd.write("0")
    seqfd.close()
