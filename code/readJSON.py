import json

def loadJsonType(filename):

	def loadJson(filename):
		with open(filename, 'r') as file:
			return json.load(file)
			
	data = loadJson(filename)
	def getSecrets(name):
		for secret in data['secrets']:
			if secret['name'] == name:
				return secret['value']
		return None

	def getXorKeys(name):
		for xorKey in data['xorKeys']:
			if xorKey['name'] == name:
				return xorKey['value'], xorKey.get('type')
		return None, None

	def getSalt(name):
		for salt in data['salts']:
			if salt['name'] == name:
				return salt['value']
		return None