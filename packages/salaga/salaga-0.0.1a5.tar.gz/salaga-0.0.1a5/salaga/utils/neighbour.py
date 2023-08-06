import random
import salaga.utils.slgcodes as scd


def getNeighbour():
    try:
        neigh = open(scd.SLGCONF+"/neighbours.list", "r")
    except Exception as e:
        neigh = open(scd.SLGCONF+"/neighbours.list", "w")
        neigh.write(scd.myIP)
        neigh.close()
    finally:
        neigh = open(scd.SLGCONF+"/neighbours.list", "r")
        neighbours = neigh.readlines()
        neigh.close()
        return(random.choice(neighbours))
