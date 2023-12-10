import discord
from discord.ext import commands
import hashlib
import locale
from datetime import datetime, timedelta
import client_data
import random
import string
import os
import subprocess
import mongo
import re

async def isAuthor(received_id: str, owner_id: str):
    adminlist = await mongo.getadmin()
    if str(received_id) == owner_id or str(received_id) in adminlist['data']:
        response = {
            'status': 200,
            'message': 'Authorized!'
        }
        return response
    else:
        response = {
            'status': 400,
            'message': 'Unauthorized!'
        }
        return response
    
async def timenow():
    current_time_utc = datetime.utcnow()
    gmt_offset = timedelta(hours=7)  # GMT+7 offset
    current_time_gmt7 = current_time_utc + gmt_offset
    formatted_time = current_time_gmt7.strftime("%Y/%m/%d at %I:%M %p")
    return formatted_time

def rupiah_format(angka, with_prefix=False, desimal=2):
    try:
        rupiah = f'{angka:,.2f}'  # Formats as currency with 2 decimal places and comma separators for thousands
        return rupiah
    except:
        return angka

def generatemd5(input_string):
    encoded_string = input_string.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_string)
    hashed_string = md5_hash.hexdigest()

    return hashed_string

def getonemonth():
    current_date = datetime.now()

    # Add one month to the current date
    one_month_later = current_date + timedelta(days=30)  # Adds 30 days for simplicity

    # Format the date as "date-month-year"
    formatted_date = one_month_later.strftime('%d-%m-%Y')

    return formatted_date

def addonemonth(timenow):
    current_date = datetime.strptime(timenow, '%d-%m-%Y')

    # Add one month to the current date
    one_month_later = current_date + timedelta(days=30)  # Adds 30 days for simplicity

    # Format the date as "date-month-year"
    formatted_date = one_month_later.strftime('%d-%m-%Y')

    return formatted_date

def generate_random_string(length):
    # Define the characters you want to include in the random string
    characters = string.ascii_letters + string.digits  # Includes both uppercase and lowercase letters, and digits

    # Generate a random string of specified length
    random_string = ''.join(random.choice(characters) for i in range(length))

    return random_string

def expired(date_string):
    # Convert the given date string to a datetime object
    given_date = datetime.strptime(date_string, '%d-%m-%Y')

    # Get the current date
    current_date = datetime.now()

    # Compare the given date with the current date
    if current_date > given_date:
        return True  # The given date has passed
    else:
        return False  # The given date has not passed

async def startbot(secretkey: str):
    check = await mongo.checksecret(secretkey)
    if check['status'] == 200:
        directory_path = "/home/ubuntu/Project/DiscordRadarStore/src"
        os.chdir(directory_path)

        command = f"pm2 start main.py --interpreter=python3 --name {secretkey} -- {secretkey}"
        subprocess.run(command, shell=True, check=True)

        return {'status': 200, 'message': 'Success, try checking your bot now!'}
    else:
        return {'status': 400, 'message': check['message']}
    
async def offbot(secretkey: str):
    check = await mongo.checksecret(secretkey)
    if check['status'] == 200:
        command = f"pm2 delete {secretkey}"
        subprocess.run(f"{command}", shell=True)
        return {'status': 200, 'message': 'Success, try check your bot now!'}
    else:
        return {'status': 400, 'message': check['message']}
    
async def restartbot(secretkey: str):
    check = await mongo.checksecret(secretkey)
    if check['status'] == 200:
        command = f"pm2 restart {secretkey}"
        subprocess.run(f"{command}", shell=True)
        return {'status': 200, 'message': 'Success, try check your bot now!'}
    else:
        return {'status': 400, 'message': check['message']}
    
async def write_text_file(text, textname):
    directory_path = '/home/ubuntu/txtfiles'  # Replace this with your desired directory path
    file_name = f'{textname}.txt'
    file_content = text

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # File path
    file_path = os.path.join(directory_path, file_name)

    # Write content to the file
    with open(file_path, 'w') as file:
        file.write(file_content)

    return file_path

async def delete_text_file(textname):
    file_path_to_delete = f'/home/ubuntu/txtfiles/{textname}.txt'  # Replace with the file path you want to delete

    try:
        os.remove(file_path_to_delete)
        return True  # File deleted successfully
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}")
        return False
    
async def product_id_exists(arr, product_id):
    for item in arr:
        if 'productId' in item and item['productId'] == product_id:
            return True  # Found the 'productid' named 'cid'
    return False

async def format_number(num):
    num_str = str(num)
    if num_str.endswith('.0'):
        return num_str[:-2]  # Removing the last two characters (.0)
    else:
        return num_str
    
async def convert_id(user_id):
    return ''.join(filter(str.isdigit, user_id))

async def add_hours(hours):
    current_time = datetime.utcnow() + timedelta(hours=7)  # Adding 7 hours to convert to GMT+7
    future_time = current_time + timedelta(hours=hours)
    return future_time

async def seconds_until_future_time(future_timestamp):
    future_time = datetime.strptime(future_timestamp, "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.now()
    time_difference = future_time - current_time
    seconds_left = time_difference.total_seconds()
    return max(0, seconds_left)

async def parse_amount_and_type(input_string):
    parts = input_string.split(maxsplit=1)
    result = {}

    if len(parts) >= 2:
        amount = parts[0]
        _type = parts[1]
        try:
            if _type.strip() not in ['Diamond Lock', 'World Lock']:
                result['status'] = 400
                result['error'] = "Invalid item type"
                return result
            
            multiplier = 1

            if _type.strip() == 'Diamond Lock':
                multiplier = 100

            amount = int(amount)  # Convert the amount to an integer
            result['status'] = 200
            result['amount'] = amount * multiplier
        except ValueError:
            result['status'] = 400
            result['error'] = "Invalid format for the amount."
    else:
        result['status'] = 400
        result['error'] = "Invalid input format"

    return result