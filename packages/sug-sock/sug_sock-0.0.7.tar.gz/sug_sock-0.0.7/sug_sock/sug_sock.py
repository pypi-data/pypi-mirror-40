'''
socket extention api.
builds on the standart socket library and adds more advance functions,
making it easier to make more varied sockets.

so the sugsock would contain a regular socket object, with easy functions
stuff in a sock:
	port
	ip
	protocol
	ip type

in addition to that sug sock will have an attributes module
this attributes will be able to hold an attribut name and data.
so if i want to store the socket or peer name i could store them on the socket attributes

so i need to make a protocol for this, so sockets will know what to except
'''
#attempt to import sockets
try:
	import socket
except:
	print("[-] socket library not found")
	exit(1)
#attempt to import threads
try:
    import threading
except:
	print("[-] threading library not found")
	exit(1)
#attempt to import attributes
try:
	from Attribute import *
except:
	print("[-] Attribute module not found")
	exit(1)
	

#sugsock class
class sugsock:
	# so a call for a sugsock object goes like sugsock(ip,port,protocol,type), enter 0 or nothing for defult
	def __init__(self, ip = '0' , port = 0 , proc = 'tcp',type = 'v4'):
		try:
			if proc == 'tcp':
				if type == 'v4':
					self.sock = socket.socket()
				elif type == 'v6':
					self.sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
			if proc == 'udp':
				if type == 'v4':
					self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
				elif type == 'v6':
					self.sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
			#if the port and ip were added on creation
			if (ip !='0')and(port != 0):
				self.sock.bind(port)
			#create self properties
			self.attributes = []
			self.ip = ip
			self.port = port
			self.proc = proc
			self.type = type
			self.threads = True
		#what fucked up now
		except Exception as e:
			print("[-] an error has occured in creating the sugsock. recheck values")
			print(str(e))
		return		
	def setIp(self,ip):
		try:
			self.ip = ip
		except Exception as e:
			print("[-] an error has occured in assaigning ip to the sugsock. recheck values")
			print(str(e))	
	def bind(self,ip,port):
		try:
			self.sock.bind(port)
			self.ip = ip
			self.port = port
		except Exception as e:
			print("[-] an error has occured in binding the sugsock. recheck values")
			print(str(e))
		return
	def addAttribute(self,name,attribute):
		try:
			a = attr(name,attribute)
			self.attributes.append(a)
		except:
			print("[-] attribute addition has failled.")
		return
	def getAttribute(self,name):
		try:
			for x in range(0,len(self.attributes)):
				if self.attributes[x].name == name:
					val = self.attributes[x].value
					return val
			print("[-] getAttribute -  attribute to be returned not found.")
			return None
		except:
			print("[-] get attribute procces has failled")
			return None
	def changeAttribute(self,name,attribute):
		try:
			for x in range(0,len(self.attributes)):
				if self.attributes[x].name == name:
					self.attributes[x].value = attribute
					return 
			print("[-] changeAttribute - attribute to be changed not found.")
			return
		except:
			print("[-] change attribute procces has failled")
			return None
	#use threads to send and recive or not
	def background(self,state):
		try:
			if state == True:
				self.threads = True
			elif state == False:
				self.threads = False
		except:
			print("background function uses boolean")
		return
	#connect to external port send some stuff and disconnect
	def sendTo(self,Add,data):#############################################################
		try:
			if self.threads:
				t= Thread(target = senddata,args = (self,Add,data))
				t.start()
			else:
				senddata()
		except Exception as e:
			print("[-] an error has occured in sendTo")
			print(str(e))
		return
			
	'''def senddata(self,Add,data):
		sk = self.sock
		sk.connect()# --------------------------------------------------------------------------------------'''