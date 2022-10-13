#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ssl
import socket
import argparse
import datetime

argparser = argparse.ArgumentParser()
argparser.add_argument('--host', help='The host to check the SSL certificate of (eg. www.google.ca)', required=True)
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

print("The certificate will expire on {}".format(expiry_date))