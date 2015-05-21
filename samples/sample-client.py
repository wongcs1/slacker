import requests
import json

# get an item from the sample-svc
my_item = requests.get('http://localhost:8080/?item=0').json()

print(my_item['foo'])

#modify the local copy of the item
my_item['foo'] = 'baz'
my_item['quux'] = 4

# push update to server
heads = {'Content-Type' : 'application/json'}
requests.put('http://localhost:8080/', headers=heads, data=json.dumps(my_item))

# create a new item
new = {'spam'  : 'eggs'}
resp = requests.post('http://localhost:8080/', headers=heads, 
                      data=json.dumps(new))
item_id = resp.json()['item']
#now delete it
requests.delete('http://localhost:8080/?item=' + str(item_id))
 
