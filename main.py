import vkDisplay
import messageThreads
import threading
import auth
import sys
import signal

def resizeHandler(a, b):
	vkDisplay.clearDisplay()
	vkDisplay.initWindow()
	messageThreads.vkConversation(0).resizeHandler()

def inputLoop():
	messageThreads.vkConversation(sys.argv[1]).initConversation()

	typedString = ''
	columns = vkDisplay.getTerminalSize()['columns']
	while True:
		sym = sys.stdin.read(1)
		if(ord(sym) == 3): break
		elif(ord(sym) == 13): 
			messageThreads.vkConversation().sendMessage(typedString)
			typedString = ''
		elif(ord(sym) == 23):
			typedString = ' '.join(typedString.split(' ')[:-1])
		elif(ord(sym) == 8 and len(typedString) > 0): 
			typedString = typedString[:-1]
		elif(32 <= ord(sym) <= 125 or 1040 <= ord(sym) <= 1103):
			typedString += sym
		vkDisplay.stdoutWrapper().write('\r\033[5C\033[K' + typedString[-columns + 7:])
	messageThreads.vkConversation().stopLongPolling()
	vkDisplay.stdoutWrapper().write('\n\r\033[2J\033[H\r')
	print('Waiting for long polling thread...\r')

if __name__ == '__main__':
	signal.signal(signal.SIGWINCH, resizeHandler)
	if(int(sys.argv[1]) > 0):
		vkDisplay.initDisplay(inputLoop)
