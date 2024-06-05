import os
line_channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
line_channel_secret = os.environ.get('LINE_CHANNEL_SECRET')

# imgur key
client_id = os.environ.get('IMGUR_CLIENT_ID')
client_secret = os.environ.get('IMGUR_CLIENT_SECRET')
album_id = os.environ.get('IMGUR_CLIENT_ALBUM_ID')
access_token = os.environ.get('IMGUR_CLIENT_ACCESS_TOKEN')
refresh_token = os.environ.get('IMGUR_CLIENT_REFRESH_TOKEN')

# DB
from pymongo import MongoClient
mongodb_token = os.environ.get('MONGODB_TOKEN')
mongo_client = MongoClient(mongodb_token)

# GeminiAI
Gemini_api_key = os.environ.get('Gemini_api_key')
