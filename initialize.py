import ConfigParser
import uuid
import couchdb
from couchdb.http import basic_auth
from getpass import getpass
import urllib2
import json
couch = couchdb.Server()
all_headers = couch.resource.headers.copy()

config = ConfigParser.RawConfigParser()
config.read("hwidgets.conf")
try:
    usern = config.get("Server","username")
    pw = config.get("Server","password")
    couch.resource.credentials = (usern,pw)
except ConfigParser.NoOptionError:
    usern = "hwidgets" 
    pw = str(uuid.uuid4()).replace("-","")
    config.set("Server","password", pw)
    username = raw_input("Username leave blank if none: ")
    if not username == "":
        password = getpass("Password: ")
        couch.resource.credentials = (username,password)
	authorization = basic_auth(couch.resource.credentials)
	if authorization:
	    all_headers['Authorization'] = authorization
	all_headers["Content-Type"] = "application/json"
    url = "http://localhost:5984/_config/admins/"+usern
    data = pw
    request = urllib2.Request(url, data=json.dumps(data), headers=all_headers)
    request.get_method = lambda: 'PUT'
    try:
        urllib2.urlopen(request)
    except urllib2.HTTPError:
        pass
    couch.resource.credentials = (usern,pw)
    with open("hwidgets.conf", "wb") as configfile:
        config.write(configfile)

if not "wifi" in couch:
    couch.create("wifi")
if not "battery" in couch:
    couch.create("battery")

authorization = basic_auth(couch.resource.credentials)
if authorization:
    all_headers['Authorization'] = authorization
all_headers["Content-Type"] = "application/json"

config_changes = [
    ("http://localhost:5984/_config/httpd/enable_cors", "true"),
    ("http://localhost:5984/_config/cors/origins", "*"),
    ("http://localhost:5984/_config/cors/credentials", "true"),
    ("http://localhost:5984/_config/cors/methods",
     "GET, PUT, POST, HEAD, DELETE"),
    ("http://localhost:5984/_config/cors/headers",
     "accept, authorization, content-type, origin")
]
for conf in config_changes:
    url, data = conf
    request = urllib2.Request(url, data=json.dumps(data), headers=all_headers)
    request.get_method = lambda: 'PUT'
    try:
        urllib2.urlopen(request)
    except urllib2.HTTPError:
        pass

#print(couch.config())
