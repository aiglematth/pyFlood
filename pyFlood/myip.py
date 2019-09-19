#Auteur --> aiglematth

#Imports
import netifaces

#Classe decouverte de notre Ip
class discoverMyIp():
	def __init__(self):
		self.ip = self.discoverIp()
	
	def discoverIp(self):
		for interf in netifaces.interfaces():
			for (interfType, ip) in netifaces.ifaddresses(interf).items():
				if interfType == (netifaces.AF_INET or netifaces.AF_INET6) and ip[0]["addr"] != ("127.0.0.1" or "::1" or "localhost"):
					return ip[0]["addr"]
				else:
					pass

if __name__ == "__main__":
	ip = discoverMyIp().ip
	print(ip)