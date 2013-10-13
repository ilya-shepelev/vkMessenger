import vkDisplay
import vkApi
import vkUtils
import threading

class vkConversation(object):
	_instance = None
	def __new__(class_, *args, **kwargs):
		if not isinstance(class_._instance, class_):
			class_._instance = object.__new__(class_)
			class_._instance.__initialized = False
		return class_._instance

	def __init__(self, uid):
		if(self.__initialized): return
		self.printWrapper = vkDisplay.stdoutWrapper()
		self.uid = uid
		self.vkAPI = vkApi.vkAPI()
		self.conversation = {}
		self.messageLoaderThread = vkMessageLoader(self.vkAPI, self.uid, self.conversation)
		self.__initialized = True
		# self.longPollingThread = 

	def printConversation(self):
		messageBuffer = vkUtils.formatMessages(self.conversation)

		self.printWrapper.write('\033[s')
		self.printWrapper.write('\033[2;0H') #set cursor to second line

		for message in messageBuffer[:-1]:
			self.printWrapper.write(message + '\n\r')
		self.printWrapper.write(messageBuffer[-1] + '\r')

		self.printWrapper.write('\033[u')

	def initConversation(self):
		self.messageLoaderThread.start()
		self.messageLoaderThread.join()

		self.printConversation()

	def resizeHandler(self):
		self.printConversation()

class vkMessageLoader(threading.Thread):
	def __init__(self, vkAPIHandler, uid, conversation):
		threading.Thread.__init__(self)
		self.vkAPIHandler = vkAPIHandler
		self.uid = uid
		self.conversation = conversation
			
	def run(self):
		conversationNames = [self.vkAPIHandler.getUsers([])['response'][0], self.vkAPIHandler.getUsers([self.uid])['response'][0]]
		apiMessageResponse = self.vkAPIHandler.getMessagesHistory(100, self.uid)['response']

		self.conversation['names'] = conversationNames
		self.conversation['messageHistory'] = apiMessageResponse

