from dotenv import load_dotenv
load_dotenv()
import json

with open('config.json', 'r') as file:
    config_data = json.load(file)


SECRET_KEY = config_data["SECRET_KEY"]
TOKEN = "MTE3NjM3NjIwNTc3NjI3NzU3NA.Gx9Z4h.YOY6XEzTCH0BgrFAvjBNxVPRS4xHCKMpDkRIWw"
OWNER_ID = "209222461357686795"
PRESENCE = config_data["PRESENCE"]
MONGO_URL = config_data['MONGO_URL']
ADMINSTOCK_CHANNEL = config_data['ADMINSTOCK_CHANNEL']
    



