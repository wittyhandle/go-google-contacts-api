#!/usr/bin/env python

import requests
import yaml
import sys

class ContactWriter:

	GOOGLE_AUTH = 'https://www.googleapis.com/oauth2/v4/token'
	GOOGLE_CONTACT_API = 'https://www.google.com/m8/feeds/contacts/default/full/?alt=json&max-results=30000'

	def __init__(self):

		with open('./config.yml', 'r') as f:
			cfg = yaml.load(f)

		self.get_contacts(cfg)

	def get_contacts(self, cfg):
		access_token = self.authenticate(cfg)
		authorization = "Bearer {0}".format(access_token)

		header = {'Authorization': authorization}
		contacts = requests.get(ContactWriter.GOOGLE_CONTACT_API, headers=header)

		print contacts.text

	def authenticate(self, cfg):

		params = {
			'client_id': cfg['client_id'], 
			'client_secret': cfg['client_secret'], 
			'refresh_token': cfg['refresh_token'], 
			'grant_type': 'refresh_token'
		}

		try:
			auth = requests.post(ContactWriter.GOOGLE_AUTH, params)
			auth.raise_for_status()
			return auth.json()['access_token']
		except Exception as ex:
			template = "Could not authenticate to google. Check for a valid refresh token. Details:\n{0}"
			print template.format(ex.args)
			sys.exit(1)
		

ContactWriter()