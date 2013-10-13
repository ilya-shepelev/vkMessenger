import urllib.request
import urllib.parse
import json
import re
import auth

class vkAPI():
	def __init__(self, access_token = auth.access_key):
		self.vkAPIString = "https://api.vk.com/method/%s?%s&access_token=%s&v=5.0"
		self.access_token = access_token

	def createRequest(self, method, parameters):
		return self.vkAPIString % (method, parameters, self.access_token)

	def sendMessage(self, message, user_id):
		parametersStr = "user_id=%s&message=%s" % (user_id, urllib.parse.quote(message))
		response = self.executeRequest("messages.send", parametersStr)
		return (response)

	def getFriends(self, user_id):
		parametersStr = "user_id=%s&order=name&fields=online,name&name_case=ins" % (user_id)
		response = self.executeRequest("friends.get", parametersStr)
		return (response)

	def getUsers(self, user_ids):
		if(len(user_ids) > 0): 
			parametersStr = "user_ids=%s" % (','.join(user_ids)) 
		else:
			parametersStr = ''
		response = self.executeRequest("users.get", parametersStr)
		return (response)

	def getMessages(self, count, filters, last_message_id = 0, out = 0):
		parametersStr = "count=%s&filters=%s&last_message_id=%s&out=%s" % (count, filters, last_message_id, out)
		response = self.executeRequest("messages.get", parametersStr)
		return (response)

	def getLongPollingServer(self):
		response = self.executeRequest("messages.getLongPollServer", "")
		return (response)

	def getMessagesHistory(self, count, user_id, start_message_id=0):
		parametersStr = "count=%s&user_id=%s&start_message_id=%s" % (count, user_id, start_message_id)
		response = self.executeRequest("messages.getHistory", parametersStr)
		return (response)

	def getDialogs(self, count):
		response = self.executeRequest("messages.getDialogs", "count=%s" % (count))
		return (response)

	def executeRequest(self, method, parameters):  #TODO: Improve stability
		request = self.createRequest(method, parameters)
		jsonResponse = {'response': 0}
		try:
			response = urllib.request.urlopen(url=request, timeout=20)
			jsonResponse = json.loads(response.read().decode())
			response.close()
		except:
			print("Something is wrong")
		finally:
			return (jsonResponse)

	def makeLongPoll(self):
		jsonResponse = []

		lp_server = self.getLongPollingServer()['response']
		uri = "http://%s?act=a_check&key=%s&ts=%s&wait=10&mode=0" % (lp_server['server'], lp_server['key'], lp_server['ts'])

		try:
			response = urllib.request.urlopen(url=uri, timeout=30)
			jsonResponse = json.loads(response.read().decode())['updates']
		except:
			pass
		finally:
			return (jsonResponse)


		