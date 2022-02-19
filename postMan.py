import requests
import pprint

# # create a new user
# data = {'username': 'ClarkKent'}
# res = requests.post('http://localhost:5000/api/iam/', data=data)

# # update an existing user
# data = {'username': 'SuperMan'}
# res = requests.put('http://localhost:5000/api/iam/ClarkKent', data=data)

# deleting an existing user
res = requests.delete('http://localhost:5000/api/iam/SuperMan')

print(res)
pprint.pprint(res.json())

