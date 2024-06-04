from pymongo import MongoClient
from gridfs import GridFS
from PIL import Image
import io

client = MongoClient('localhost', 27017)
db = client['plants']
fs = GridFS(db)
col = db['plants']

if __name__ == "__main__":
    for document in col.find({}):
        print(document["plant_name"])