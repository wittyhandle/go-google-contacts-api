#!/usr/bin/env python

import requests
import yaml
import sys

class ContactWriter:

	client_id = None
	client_secret = None
	refresh_token = None
	google_auth = None
	google_contact_api = None

	def __init__(self):

		with open('./config.yml', 'r') as f:
			cfg = yaml.load(f)

		with open('./secrets.yml', 'r') as f:
			secrets = yaml.load(f)

		self.client_id = cfg['client_id']
		self.client_secret = secrets['client_secret']
		self.refresh_token = secrets['refresh_token']
		self.google_auth = cfg['google_auth']
		self.google_contact_api = cfg['google_contact_api']

		self.get_contacts()

	def get_contacts(self):
		access_token = self.authenticate()
		authorization = "Bearer {0}".format(access_token)

		header = {'Authorization': authorization}
		contacts = requests.get(self.google_contact_api, headers=header)

		print contacts.json()

	def authenticate(self):

		params = {
			'client_id': self.client_id, 
			'client_secret': self.client_secret, 
			'refresh_token': self.refresh_token, 
			'grant_type': 'refresh_token'
		}

		try:
			auth = requests.post(self.google_auth, params)
			auth.raise_for_status()
			return auth.json()['access_token']
		except Exception as ex:
			msg = "Could not authenticate to google. Check for a valid refresh token. Details:\n{0}"
			print msg.format(ex.args)
			sys.exit(1)
		

ContactWriter()