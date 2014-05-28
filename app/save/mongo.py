__author__ = 'salas'


from pymongo import MongoClient
client = MongoClient()


db = client.test_database
try:
    client.drop_database(db)
except Exception:
    pass
collection = db.test_collection

import datetime


posts = db.posts
for i in range(10000):
    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": str(datetime.datetime.utcnow())}
    post_id = posts.insert(post)
print(post_id)

print(db.collection_names())
print(posts.find_one())
