import vkDisplay

def formatMessages(conversation):
	if(conversation == {}): return ['']
	terminalSize = vkDisplay.getTerminalSize() 

	names = { 
			"me": "%s %s" % (conversation['names'][0]['first_name'], conversation['names'][0]['last_name']),
			"him": "%s %s" % (conversation['names'][1]['first_name'], conversation['names'][1]['last_name'])
			}
	messages = []

	messageBuffer = ''
	for message in reversed(conversation['messageHistory']['items']):
		message['text'] = message['body']

		try: message['fwd_messages']
		except: pass
		else: message['text'] = "→ Forwarded"

		try: message['attachments']
		except: pass
		else: 
			message['text'] = message['body'] + " → Attachments"

		message['text'] = message['text'].replace('<br>', '\n').replace('\n', '\n\r')

		if(message['out']):
			messageBuffer += ('\033[31m >>> \033[0m%s: %s\n\r' % (names['me'], message['text']))
		else:
			messageBuffer += ('\033[34m <<< \033[0m%s: %s\n\r' % (names['him'], message['text']))
	

	longLines = 0

	messageBuffer = messageBuffer.split('\n\r')[-terminalSize['rows'] + 1:]
	for message in messageBuffer:
		longLines += int((len(message) - 11) / terminalSize['columns'])

	messageBuffer = messageBuffer[longLines:]
	return messageBuffer

def unpackFlags(flag):
	unpackedFlags = [False for x in range(10)]
	i = 9
	for num in [2**x for x in range(9, -1, -1)]:
		if(flag == 0): return unpackedFlags
		if(flag - num >= 0):
			unpackedFlags[i] = True
			flag -= num
		i-=1
	return unpackedFlags