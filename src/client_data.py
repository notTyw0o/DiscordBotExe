from dotenv import load_dotenv
load_dotenv()
import json

with open('config.json', 'r') as file:
    config_data = json.load(file)


SECRET_KEY = config_data["SECRET_KEY"]
TOKEN = "MTE3NjExNTExNjc4NjMyNzU3Mw.GT66bV.um3M4XqEYYMTE-Gi2EJxwSx5tUkkvh7OBl_Hqc"
OWNER_ID = "927042505587957760"
PRESENCE = config_data["PRESENCE"]
MONGO_URL = config_data['MONGO_URL']
    



