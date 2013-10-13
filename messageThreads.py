import vkDisplay
import vkApi
import vkUtils
import vkSound
import urllib
import threading

class vkConversation(object):
	_instance = None
	def __new__(class_, *args, **kwargs):
		if not isinstance(class_._instance, class_):
			class_._instance = object.__new__(class_)
			class_._instance.__initialized = False
		return class_._instance

	def __init__(self, uid = 0):
		if(self.__initialized): return
		self.printWrapper = vkDisplay.stdoutWrapper()
		self.uid = uid
		self.vkAPI = vkApi.vkAPI()
		self.conversation = {}
		self.longPollingCommand = {'run': False}
		self.messageLoaderThread = vkMessageLoader(self.vkAPI, self.uid, self.conversation)
		self.longPollingThread = vkLongPolling(self.vkAPI, self.conversation, self.longPollingCommand)
		self.__initialized = True

	def printConversation(self):
		messageBuffer = vkUtils.formatMessages(self.conversation)

		self.printWrapper.write('\033[s')
		self.printWrapper.write('\033[2;0H') #set cursor to second line

		for message in messageBuffer[:-1]:
			self.printWrapper.write('\033[K' + message + '\033[K\n\033[K\r')
		self.printWrapper.write('\033[5C' + messageBuffer[-1])

		self.printWrapper.write('\033[u')

	def initConversation(self):
		self.messageLoaderThread.start()
		self.startLongPolling()

	def startLongPolling(self):
		if(not self.longPollingCommand['run']): self.longPollingThread.start()

	def stopLongPolling(self):
		self.longPollingCommand['run'] = False

	def resizeHandler(self):
		self.printConversation()

	def sendMessage(self, text):
		sendThread = vkMessageSender(self.vkAPI, self.uid, self.conversation, text)
		sendThread.start()

class vkMessageSender(threading.Thread):
	def __init__(self, vkAPIHandler, uid, conversation, messageText):
		threading.Thread.__init__(self)
		self.vkAPIHandler = vkAPIHandler
		self.uid = uid
		self.conversation = conversation
		self.messageText = messageText

	def run(self):
		new_item = {'id': 0, 'body': self.messageText, 'out': 1}
		self.conversation['messageHistory']['items'].insert(0, new_item)
		vkConversation().printConversation()
		sentMessageID = self.vkAPIHandler.sendMessage(self.messageText, self.uid)
		self.conversation['messageHistory']['items'][0]['id'] = sentMessageID['response']

class vkLongPolling(threading.Thread):
	def __init__(self, vkAPIHandler, conversation, command):
		threading.Thread.__init__(self)
		self.vkAPIHandler = vkAPIHandler
		self.conversation = conversation
		self.command = command

	def run(self):
		self.command['run'] = True
		self_uid = self.vkAPIHandler.getUsers([])['response'][0]['id']
		while self.command['run']:
			updates = self.vkAPIHandler.makeLongPoll()
			if(updates != []):
				for update in updates:
					if(update[0] == 4):
						updateObj = {'body': update[6], 'id': update[1], 'from': update[3], 'out': int(update[3] == self_uid)}
						if(update[1] != self.conversation['messageHistory']['items'][0]['id']):
							self.conversation['messageHistory']['items'].insert(0, updateObj)
				vkConversation().printConversation()

class vkMessageLoader(threading.Thread):
	def __init__(self, vkAPIHandler, uid, conversation):
		threading.Thread.__init__(self)
		self.vkAPIHandler = vkAPIHandler
		self.uid = uid
		self.conversation = conversation
			
	def run(self):
		conversationNames = [self.vkAPIHandler.getUsers([])['response'][0], self.vkAPIHandler.getUsers([self.uid])['response'][0]]
		apiMessageResponse = self.vkAPIHandler.getMessagesHistory(120, self.uid)['response']

		self.conversation['names'] = conversationNames
		self.conversation['messageHistory'] = apiMessageResponse

		vkConversation().printConversation()

