# -*- coding:utf-8 -*-

from pymongo import MongoClient
from imgurpython import ImgurClient
from config import client_id, client_secret, access_token, refresh_token, mongo_client
db = mongo_client.get_database('linebot_kai')

# client = ImgurClient(client_id, client_secret, access_token, refresh_token)
#
#
# def get_pttinfo():
#     db = mongo_client.get_database('PTT')
#     record = db.beauty_data
#     q = record.aggregate([{'$sample': {'size': 1}}])
#     for x in q:
#         url = x['url']
#         rd_img = x['img']
#         title = x['title']
#     return url, rd_img, title
#
#
# def lineid_mapping(display_name, userid):
#     db = mongo_client_ccsue.get_database('linebot')
#     record = db.id_map
#     post = {str(display_name): str(userid)}
#     record.insert_one(post)
def check_mode():
    collection = db.mode
    document = collection.find_one({})
    if document and 'mode' in document:
        print(f"Mode: {document['mode']}")
        return document['mode']
    else:
        
        return None


def mode_change(mode_cmd):
    collection = db.mode
    
    if mode_cmd == "quiet":
        new_mode = "quiet"
    elif mode_cmd == "talking":
        new_mode = "talking"
    else:
        print("")
        return

    # update 
    result = collection.update_one(
        {},  
        {'$set': {'mode': new_mode}}
    )

    if result.matched_count > 0:
        print(f"mode revise to {new_mode}")
    else:
        print("Not find")
mode_change("quiet")