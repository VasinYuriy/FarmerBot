from pymongo import MongoClient
from gridfs import GridFS
from PIL import Image
import io
filename = "currant.jpg"

# Подключение к MongoDB
client = MongoClient('localhost', 27017)
db = client['plants']
fs = GridFS(db)
col = db['plants']

# Открываем исходное изображение
with open(filename, 'rb') as f:
    photo_data = f.read()


# Сохраняем фото в GridFS
photo_id = fs.put(photo_data, filename=filename)

print("Фото сохранено в MongoDB с идентификатором:", photo_id)
