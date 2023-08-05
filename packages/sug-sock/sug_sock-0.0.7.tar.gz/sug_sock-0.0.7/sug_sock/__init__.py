'''
socket extention api.
builds on the standart socket library and adds more advance functions,
making it easier to make more varied sockets.
'''
#attempt to import sug_sock
try:
	from sug_sock import *
except:
	print('[-] sug_sock library not found')
	exit(1)
'''
#attempt to import threads
try:
	from threading import *
except:
	print('[-] Thread library not found')
	exit(1)
'''
#generic debug function
def debug():
	print('debug function: ')
	print(dir('sug_sock')) 
	#print(dir(os))
	#print(os.getcwd())

#nice meme
def meme():
	print("nice")
#another debug function
def test():
	a = sugsock()
	print(str(a.ip))
	print(str(a.port))
	print(str(a.proc))
	print(str(a.type))
	a.addAttribute('name','boop')
	print(str(a.getAttribute('name')))
	a.changeAttribute('name' , 'doop')
	print(str(a.getAttribute('name')))
#debug()
test()