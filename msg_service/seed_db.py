from pymongo import MongoClient

seed_msg = [
        {'message_id': 1, 'channel_id': 1, 'user_id': 1, 'body': 'Hello user', 'timestamp': 1432279234},
        {'message_id': 2, 'channel_id': 1, 'user_id': 2, 'body': 'Why hello there', 'timestamp': 1432279237},
        {'message_id': 3, 'channel_id': 1, 'user_id': 1, 'body': 'I really was hoping not to see you today', 'timestamp': 1432279240},
        {'message_id': 4, 'channel_id': 1, 'user_id': 2, 'body': 'Likewise.', 'timestamp': 1432279247}
        ]

# DB running on default host/port
client = MongoClient()

# Selects a message_database
db = client.message_database

# Selects a collection, ensures empty
collection = db.messages
collection.delete_many({})

# Insert seed messages
collection.insert_many(seed_msg)

# Print entered messages
for m in collection.find():
    print m

