import imgurpython
import random

class ImgurLink:
	def __init__(self):
		self.client = self.login()
	
	def login(self):
		client_id = ''
		client_secret = ''
		client = imgurpython.ImgurClient(client_id, client_secret)
		return client

	def return_link(self, query):
		items = self.client.gallery_search(query)
		item_link = random.choice(items).link
		return(item_link)
	