#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ssl
import socket
import argparse
import datetime

argparser = argparse.ArgumentParser()
argparser.add_argument('--host', help='The host to check the SSL certificate of (eg. www.google.ca)', required=True)
argparser.add_argument('--warning_threshold', help="""Only display a certificate expiry warning if the certificate is
	due to expire in less than or equal to WARNING_THRESHOLD days.""", type=int, default=-1)
args = argparser.parse_args()

def getSSLCert(hostname, port=443):
	ctx = ssl.create_default_context()
	conn = ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
	conn.connect((hostname, port))
	ssl_info = conn.getpeercert()
	conn.close()
	return ssl_info

def getCertificateDate(certificate, field_name):
	return datetime.datetime.strptime(certificate[field_name], '%b %d %H:%M:%S %Y %Z')

ssl_cert = getSSLCert(args.host)
expiry_date = getCertificateDate(ssl_cert, 'notAfter')

timedelta_until_expiry = expiry_date - datetime.datetime.now()
days_until_expiry = timedelta_until_expiry.days

if (args.warning_threshold < 0) or (days_until_expiry <= args.warning_threshold):
	print("The certificate will expire in {} days".format(days_until_expiry))
