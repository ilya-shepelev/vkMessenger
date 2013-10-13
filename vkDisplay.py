import sys
import os
import tty
import termios
import threading

class stdoutWrapper(object):
	_instance = None
	def __new__(class_, *args, **kwargs):
		if not isinstance(class_._instance, class_):
			class_._instance = object.__new__(class_)
			class_._instance.__initialized = False
		return class_._instance

	def __init__(self):
		if(self.__initialized): return
		self.printLock = threading.Lock()
		self.__initialized = True

	def write(self, string):
		with self.printLock:
			sys.stdout.write(string)
		sys.stdout.flush()

def initDisplay(inputLoop):
	fd = sys.stdin.fileno()
	tOldState = termios.tcgetattr(fd)
	tty.setraw(fd)

	clearDisplay()
	initWindow()
	try:
		if(hasattr(inputLoop, '__call__')):
			inputLoop()
	except(e):
		print(e)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, tOldState)

def getTerminalSize():
	rows, columns = os.popen('stty size', 'r').read().split();
	return {'rows': int(rows), 'columns': int(columns)}

def moveCursorLR(count):
	stdoutWrapper().write(('\033[%iC' % count) if count > 0 else ('\033[%iD' % count * -1))

def moveCursorHome():
	stdoutWrapper().write('\033[H')

def clearDisplay():
	stdoutWrapper().write('\033[2J')

def setCursorPos(y, x):
	stdoutWrapper().write('\033[%i;%iH' % (x, y))

def drawHeaderLine(text):
	stdoutWrapper().write('\033[s') #save cursor pos
	moveCursorHome()
	stdoutWrapper().write('\033[30;47m\033[2K') #set colors and clean line
	moveCursorLR(int((getTerminalSize()['columns'] - len(text)) / 2)) #moving to center
	stdoutWrapper().write(text)
	stdoutWrapper().write('\033[u') #return cursor back

def initWindow():
	drawHeaderLine("vkMessenger")
	setCursorPos(0, getTerminalSize()['rows']) #moving to bottom left corner
	stdoutWrapper().write('\033[0;31m >>> \033[0m')


