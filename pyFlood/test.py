from cmd import Cmd
from sys import exit
from shlex import split
import floods
if __name__ == "__main__":
    a = floods.IcmpFlood()
    a.ipSpoof = "192.168.1.1"
    a.searchBroadcast()
    print(a.broadcast)
