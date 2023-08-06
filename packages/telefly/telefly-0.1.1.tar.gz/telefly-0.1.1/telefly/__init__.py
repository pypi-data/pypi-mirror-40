import requests
import json
import urllib


class telefly:
	def __init__(self, token):
		self.URL = "https://api.telegram.org/bot{}/".format(token)
		
	
	""" downloads the content from a URL and gives us a string """
	def getUrl(self, url):
		response = requests.get(url)
		content = response.content.decode("utf8")	# .decode("utf8") for extra compatibility
		return content
		
	def postUrl(self, url, files):
		response = requests.post(url, files=files)
		content = response.content.decode("utf8")
		return content
	
	
	""" parses the JSON response (content) into a Python dictionary """
	def getJson(self, url):
		content = self.getUrl(url)
		js = json.loads(content)
		return js
		
		
	""" retrieves a list of "updates" (aka. Messages to our bot) """
	def getUpdates(self, offset=None):	# offset is the last update id
		url = self.URL + "getUpdates?timeout=100"	# using Long Polling to prevent high requests
		if offset:
			url += "&offset={}".format(offset)	# with the offset parameter the api sends only the newer updates
		js = self.getJson(url)
		return js
		
	""" calculates the highest ID of all the updates """
	def getLastUpdateId(self, updates):
		update_ids = []
		for update in updates["result"]:
			update_ids.append(int(update["update_id"]))
		return max(update_ids)
		
	
	""" sends an action like 'typing'
		'typing' for text messages, 
		'upload_photo' for photos, 
		'record_video' or 'upload_video' for videos, 
		'record_audio' or 'upload_audio' for audio files, 
		'upload_document for general files, 
		'find_location' for location data, 
		'record_video_note' or 'upload_video_note' for video notes.
	"""
	def sendAction(self, chat_id, action):
		url = self.URL + "sendChatAction?action={}&chat_id={}".format(action, chat_id)
		self.getUrl(url)
		
	
	""" sends text to chat_id
		parse_mode:
			'Markdown' or 'HTML'
	"""
	def sendMessage(self, text, chat_id, disable_notification=None, parse_mode=None, reply_markup=None):
		text = urllib.parse.quote_plus(text)			# encode any special characters in our message to be url-friendly, for example the + sign
		url = self.URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
		if disable_notification:
			url += "&disable_notification={}".format(disable_notification)
		if parse_mode:
			url += "&parse_mode={}".format(parse_mode)
		if reply_markup:
			url += "&reply_markup={}".format(reply_markup)
		self.getUrl(url)
		
	
	""" creates a keyboard to give it sendMessage """
	def buildKeyboard(self, items):
		keyboard = [[item] for item in items]
		reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
		return json.dumps(reply_markup)
		
	""" sends a picture to chat_id """
	def sendPicture(self, chat_id, filename):
		url = self.URL + "sendPhoto?chat_id={}".format(chat_id)
		files = {'photo': open(filename, 'rb')}
		self.postUrl(url, files)
			
		
# TODO: All the other methods of Telegram bots https://core.telegram.org/bots/api
#		Important: forceReply, sendVideos, parseMode, (inline)Keyboards,
#		reply_to_message_id, edit message ...

