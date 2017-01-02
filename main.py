#!/usr/bin/env python

import requests
import yaml
import sys
import csv

class ContactWriter:

	client_id = None
	client_secret = None
	refresh_token = None
	google_auth = None
	google_contact_api = None

	def __init__(self):

		fout = open("./out.txt", 'a')

		with open('./config.yml', 'r') as f:
			cfg = yaml.load(f)

		with open('./secrets.yml', 'r') as f:
			secrets = yaml.load(f)

		self.client_id = cfg['client_id']
		self.google_auth = cfg['google_auth']
		self.google_contact_api = cfg['google_contact_api']
		self.client_secret = secrets['client_secret']
		self.refresh_token = secrets['refresh_token']
		
		contacts = self._get_contacts()

		csv_entries = []
		for entry in contacts['feed']['entry']:
			if 'gd$email' in entry and 'title' in entry and entry['title']['$t'] != '':
				name = entry['title']['$t']
				email = entry['gd$email'][0]['address']
				csv_entries.append({'name': name, 'email': email})

		keys = csv_entries[0].keys()
		with open('contacts.csv', 'wb') as f:
			dict_writer = csv.DictWriter(f, keys)
			dict_writer.writeheader()
			dict_writer.writerows(csv_entries)

	def _get_contacts(self):
		access_token = self._authenticate()
		authorization = "Bearer {0}".format(access_token)

		header = {'Authorization': authorization}
		contacts = requests.get(self.google_contact_api, headers=header)

		return contacts.json()

	def _authenticate(self):

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