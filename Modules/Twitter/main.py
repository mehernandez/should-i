import json
import base64
import io
from httplib import *

CONSUMER_KEY = None
PRIVATE_KEY = None
BEARER_TOKEN = None
baseURL = "api.twitter.com"
connection = HTTPSConnection(baseURL)

def getToken():
	bearerCreds = base64.b64encode(CONSUMER_KEY+":"+PRIVATE_KEY)
	headers = {"Authorization": "Basic " + bearerCreds, "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"}
	body = "grant_type=client_credentials"
	connection.request("POST","/oauth2/token",body,headers)
	response = connection.getresponse()
	if response.status == 200:
		ans = response.read()
		parsed = json.loads(ans)
		global BEARER_TOKEN
		BEARER_TOKEN = parsed["access_token"]
		print("Success")
	else:
		print("Failed")
		print(response.read())


def serializeData():
	with io.open('data.json', 'w') as f:
		jsonFile = {'CONSUMER_KEY':CONSUMER_KEY,'PRIVATE_KEY':PRIVATE_KEY,'BEARER_TOKEN':BEARER_TOKEN}
		f.write(unicode(json.dumps(jsonFile, ensure_ascii=False)))

def deserializeData():
	with io.open('data.json', 'r') as f:
		parsed = json.loads(f.readline())
		global CONSUMER_KEY
		global PRIVATE_KEY
		global BEARER_TOKEN
		CONSUMER_KEY = parsed["CONSUMER_KEY"]
		PRIVATE_KEY = parsed["PRIVATE_KEY"]
		try:
			BEARER_TOKEN = parsed["BEARER_TOKEN"]
		except:
			getToken()