import sys


def newStore():
    try:
        seqfd = open("tmp/SEQ.salgtmp", "r")
    except FileNotFoundError:
        initSEQ()
        seqfd = open("tmp/SEQ.salgtmp", "r")
    finally:
        nextseq = seqfd.read()
        if(nextseq is None):
            initSEQ()
        seqfd.close()
        seqfd = open("tmp/SEQ.salgtmp", "w")
        seqfd.write(str(int(nextseq)+1))
        seqfd.close()
        return(hash(nextseq) + sys.maxsize)


def initSEQ():
    seqfd = open("tmp/SEQ.salgtmp", "w")
    seqfd.write("0")
    seqfd.close()
