import pymongo
import PIL
from PIL import Image

client = pymongo.MongoClient("mongodb+srv://shaishavshah:srs12345@cluster1.jksay.mongodb.net/eRunner?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs='CERT_NONE')
db = client.get_database('eRunner')
records = db.user_avatar

def image(user_id):

	raw_avatar = records.find_one({'user_id': user_id})
	img2 = PIL.Image.frombytes('RGB', raw_avatar['img_size'], raw_avatar['avatar'])

	return img2

# profile_pic = image(7)
# profile_pic.show()