# Linebot

## Configuration (Modify in config.py):
- Line access token : 連結Line bot
- Imgur token       : 保存相片至imgur
- MongoDB token     : 關鍵字對話 

## Deployment:
Deploy on Render cloud (free) : https://render.com/
Enter secret keys (config keys) in Render settings

## Functions:
- Gemini AI
- Ptt Draw Card
- Auto Reply
- Image2Anime

# Artificial Intelligence:
Utilizes an API-connected model in `model_api.py`.

** Gemini API ** 
- 官方 : https://ai.google.dev/gemini-api 

**Model Information:**
- Model Name: Thin-Plate-Spline-Motion-Model Public
- GitHub Repository: [https://github.com/yoyo-nb/Thin-Plate-Spline-Motion-Model](https://github.com/yoyo-nb/Thin-Plate-Spline-Motion-Model)

---

## Important Notes:

Please note that this project requires the following three tokens to enable the respective functionalities. Please generate these tokens yourself and add them to the `config.py` file.

1. **Line Access Token:**
   - Obtain from [Line Developers Console](https://developers.line.biz/en/).

2. **Imgur Token:**
   - Get your Imgur API key from the [Imgur Developer Platform](https://api.imgur.com/oauth2/addclient).

3. **MongoDB Token:**
   - Create an account on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) or your chosen MongoDB provider and obtain your MongoDB connection string.

Ensure that you manage these tokens securely and do not share them directly on public forums or store them in insecure locations.

---
