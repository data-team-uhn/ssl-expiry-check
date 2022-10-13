#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import socket
import argparse
import datetime
import requests

argparser = argparse.ArgumentParser()
argparser.add_argument('--host', help='The host to check the SSL certificate of (eg. www.google.ca)', required=True)
argparser.add_argument('--warning_threshold', help="""Only display a certificate expiry warning if the certificate is
	due to expire in less than or equal to WARNING_THRESHOLD days.""", type=int, default=-1)
argparser.add_argument('--slack', help='Send warning messages to a Slack channel (SLACK_CHANNEL_URL environment variable must be configured)', action='store_true')
args = argparser.parse_args()

if args.slack:
	SLACK_CHANNEL_URL = os.environ['SLACK_CHANNEL_URL']

def getSSLCert(hostname, port=443):
	ctx = ssl.create_default_context()
	conn = ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
	conn.connect((hostname, port))
	ssl_info = conn.getpeercert()
	conn.close()
	return ssl_info

def getCertificateDate(certificate, field_name):
	return datetime.datetime.strptime(certificate[field_name], '%b %d %H:%M:%S %Y %Z')

def slackNotify(message):
	r = requests.post(SLACK_CHANNEL_URL, json={'text': message})
	if r.status_code != 200:
		raise Exception("Slack returned a non-200 HTTP response code")

ssl_cert = getSSLCert(args.host)
expiry_date = getCertificateDate(ssl_cert, 'notAfter')

timedelta_until_expiry = expiry_date - datetime.datetime.now()
days_until_expiry = timedelta_until_expiry.days

if (args.warning_threshold < 0) or (days_until_expiry <= args.warning_threshold):
	warning_message = "The certificate for {} will expire in {} days".format(args.host, days_until_expiry)
	print(warning_message)
	if args.slack:
		slackNotify(":identification_card: " + warning_message + " :warning:")
