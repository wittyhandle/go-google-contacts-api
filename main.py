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
	csv_location = None

	# init gets called for each instantiation of ContactWriter
	def __init__(self):

		# Open up config and secrets yaml files
		try:
			with open('./config.yml', 'r') as f:
				cfg = yaml.load(f)

			with open('./secrets.yml', 'r') as f:
				secrets = yaml.load(f)
		except Exception as ex:
			msg = "Could not load config.yml or secrets.yml configuration. Details:\n{0}"
			print msg.format(ex.args)
			sys.exit(1)

		# store configurations in instance variables
		self.client_id = cfg['client_id']
		self.google_auth = cfg['google_auth']
		self.google_contact_api = cfg['google_contact_api']
		self.csv_location = cfg['csv_location']
		self.client_secret = secrets['client_secret']
		self.refresh_token = secrets['refresh_token']
		
		# get contacts from google via the _get_contacts function
		contacts = self._get_contacts()

		csv_entries = []
		for entry in contacts['feed']['entry']:
			if 'gd$email' in entry and 'title' in entry and entry['title']['$t'] != '':
				name = entry['title']['$t']
				email = entry['gd$email'][0]['address']
				address = entry['gd$postalAddress'][0]['$t'] if 'gd$postalAddress' in entry else ''

				csv_entries.append({'name': name, 'email': email, 'address': address})

		with open(self.csv_location, 'wb') as f:
			dict_writer = csv.DictWriter(f, ['name', 'email', 'address'])
			dict_writer.writeheader()
			dict_writer.writerows(csv_entries)

		print "Successfully wrote {0} to csv file at {1}".format(len(csv_entries), self.csv_location)

	# Handles retrieving contacts from google. Returns them as json
	def _get_contacts(self):
		# get an access token from google to use to get contacts with
		access_token = self._authenticate()
		authorization = "Bearer {0}".format(access_token)

		header = {'Authorization': authorization}
		try:
			# call the google api to get the contacts
			contacts = requests.get(self.google_contact_api, headers=header)
			contacts.raise_for_status()
		except Exception as ex:
			msg = "Could not retrieve contacts from google. Details:\n{0}"
			print msg.format(ex.args)
			sys.exit(1)

		return contacts.json()

	# Performs the authentication to google by passing in client information and the refresh token
	# to get an access token
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

# Logic starts here, instantiates an instance of the ContactWriter class
ContactWriter()