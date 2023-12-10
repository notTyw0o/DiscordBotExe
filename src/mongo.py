from dotenv import load_dotenv
load_dotenv()
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import client_data
import util_function
from typing import List
import re

uri = f'{client_data.MONGO_URL}'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

def mongoConnect():
    try:
        client.admin.command('ping')
        print("Connection Established!")
    except Exception as e:
        print(e)

async def checkOwner(SECRET_KEY: str):
    SECRET_KEY = SECRET_KEY
    return {'status': 200, 'message': 'Bot is active and ready to use!'}
    
async def getPresence(SECRET_KEY: str):
    db = client["user"]
    collection = db["data"]

    CHECK = list(collection.find({
        "database": "User Data"
    }))

    RESULTS = CHECK[0].get('user_data')

    checkResult = []
    for i in RESULTS:
        if SECRET_KEY == i.get('secretkey'):
            checkResult.append(i)
            
    if len(checkResult) < 1:
        response = {
            'status': 400,
            'message': 'Null'
        }
        return response
    else:
        msg = checkResult[0].get('data').get('presence')
        response = {
            'status': 200,
            'message': msg
        }
        return response
    
def getbotinfo():
    db = client[f'user_{client_data.SECRET_KEY}']
    data = db[f'data']

    bot = data.find_one({'discordtoken': client_data.TOKEN})
    if bot is None:
        raise ValueError('Bot is not in the databases!')
    else:
        {'status': 200, 'data': bot}

async def addProduct(productName: str, productId: str, productPrice: int, roleid):
    db = client[f'user_{client_data.SECRET_KEY}']
    collection = db[f'product']

    query = {
        'productName': productName,
        'productId': productId,
        'productPrice': productPrice,
        'roleId': roleid
    }
    try:
        queryCheck = collection.find_one({
            'database': 'User Product',
        })
        if queryCheck is None:
            collection.insert_one({
                'database': 'User Product',
                'productlist': [query]
            })
        elif any(d.get('productId') == productId for d in queryCheck.get('productlist')):
            return f'Product ID is already exist in databases!'
        else:
            modified = queryCheck
            modified.get('productlist').append(query)
            update = {
                "$set": {
                    "productlist": modified.get('productlist')
                }
            }
            collection.update_one({'database': 'User Product'}, update)
        return 'Product successfully added to databases!'
    except Exception as e:
        return f'Error occurred, Please contact support!'

async def addProductLisen(productPrice: int, roleid):
    db = client[f'user_{client_data.SECRET_KEY}']
    collection = db[f'productlisen']

    data = collection.find_one({'database': 'User Product'})
    if data is None:
        query = {
            'database': 'User Product',
            'productlist': [{
                'productName': 'Lisensi Radar Bot',
                'productId': 'botlisen',
                'productPrice': productPrice,
                'roleId': roleid
            }]
        }
        collection.insert_one(query)
        return f'Success add product to databases!'
    else:
        return f'Product already exist in databases!'
    
async def removeproduct(productId: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    collection = db[f'product']
    stock = db[f'stock']

    query = collection.find_one({'database': 'User Product'})
    
    if query is None:
        return 'Not found!'
    else:
        for index, data in enumerate(query.get('productlist')):
            if data.get('productId') == productId:
                query.get('productlist').pop(index)
                break
        update = {
            "$set": {
                "productlist": query.get('productlist')
            }
        }
        collection.update_one({'database': 'User Product'}, update)
        stock.find_one_and_delete({'productId': productId})
        return 'Remove product success!'
    
async def setprice(productId: str, newPrice: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    collection = db[f'product']

    query = collection.find_one({'database': 'User Product'})
    
    if query is None:
        return 'Not found!'
    else:
        totalfound = 0
        for index, data in enumerate(query.get('productlist')):
            if data.get('productId') == productId:
                data['productPrice'] = newPrice
                totalfound = totalfound + 1
        update = {
            "$set": {
                "productlist": query.get('productlist')
            }
        }
        collection.update_one({'database': 'User Product'}, update)
        if totalfound == 0:
            return f'Product not found in the database!'
        else:
            return 'New price has been set!'
        
async def addstock(productId: str, productdetails: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'product']
    stock = db[f'stock']

    query = product.find_one({'database': 'User Product'})
    productCheck = 0 #if 0 then its False
    for data in query.get('productlist'):
        if data.get('productId') == productId:
            productCheck = productCheck + 1
            break
    
    if query is None:
        return 'Database not found!'
    elif productCheck == 0:
        return 'Product not existed in the databases!'
    else:
        stockQuery = stock.find_one({'productId': productId})
        if stockQuery is None:
            stockdata = {
                'database': 'User Stock',
                'productId': productId,
                'stock': [productdetails]
            }
            stock.insert_one(stockdata)
        else:
            stockArray = stockQuery.get('stock')
            stockArray.append(productdetails)
            update = {
                "$set": {
                    "stock": stockArray
                }
            }
            stock.update_one({'productId': productId}, update)
        return 'Stock successfully added to the databases!'
    
async def addadminstock(productdetails: str, discordid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'adminstock']

    filter = {'admin': discordid}

    data = product.find_one(filter)

    if isinstance(productdetails, str):
        productdetails = [productdetails]
    
    if data is None:
        query = {
            'database': 'User Admin Stock',
            'admin': discordid,
            'instock': productdetails,
            'sold': []
        }
        product.insert_one(query)
        return {'status': 200, 'message': 'Success added admin stock!'}
    else:
        stockArray = data['instock']
        stockArray.extend(productdetails)
        update = {
            "$set": {
                "instock": stockArray
            }
        }
        product.update_one(filter, update)
        return {'status': 200, 'message': 'Success added admin stock!'}

async def convertadminstock(productdetails: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'adminstock']

    alldata = product.find({})
    for datas in alldata:
        if productdetails[0] in datas['instock']:
            data = datas
            break

    filter = {'admin': data['admin']}
    removedstock = [item for item in data['instock'] if item not in productdetails]
    newsold = data['sold']
    newsold.extend(productdetails)
    update = {
        "$set": {
            'instock': removedstock,
            'sold': newsold
        }
    }
    product.update_one(filter, update)
    return {'status': 200, 'message': 'Success convert stock!'}

async def clearsold(discordid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'adminstock']

    filter = {'admin': discordid}
    data = product.find_one(filter)
    if data is None:
        return {'status': 400, 'message': 'User not found!'}
    else:
        update = {
            "$set": {
                'sold': []
            }
        }
        product.update_one(filter, update)
        return {'status': 200, 'message': 'Clear success!'}

async def addstocklisen(amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'productlisen']
    stock = db[f'stocklisen']

    productId = 'botlisen'
    productdetails = 'xx'

    query = product.find_one({'database': 'User Product'})
    productCheck = 0 #if 0 then its False
    for data in query.get('productlist'):
        if data.get('productId') == productId:
            productCheck = productCheck + 1
            break
    
    if query is None:
        return 'Database not found!'
    elif productCheck == 0:
        return 'Product not existed in the databases!'
    else:
        newstock = []
        for i in range(amount):
            newstock.append(productdetails)

        stockQuery = stock.find_one({'productId': productId})
        if stockQuery is None:
            stockdata = {
                'database': 'User Stock',
                'productId': productId,
                'stock': [productdetails]
            }
            stock.insert_one(stockdata)
        else:
            stockArray = stockQuery.get('stock')
            stockArray.extend(newstock)
            update = {
                "$set": {
                    "stock": stockArray
                }
            }
            stock.update_one({'productId': productId}, update)
        return 'Stock successfully added to the databases!'

async def showstock(productId: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stock']

    data = stock.find_one({'productId': productId})
    if data is None or len(data.get('stock')) == 0:
        return f'No stock found in the databases!'
    else:
        message = ''
        for index, stock in enumerate(data.get('stock')):
            message = message + stock + ' - Index ' + str(index) + '\n'

        return f'{message}'

async def removestock(productId: str, index: int, isAll: bool):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stock']

    data = stock.find_one({'productId': productId})
    if data is None:
        return f'Nothing to delete!'
    elif isAll:
        update = {
                "$set": {
                    "stock": []
                }
            }
        stock.update_one({'productId': productId}, update)
        return f'Success remove all stocks available!'
    else:
        data.get('stock').pop(index)
        modified = data.get('stock')
        update = {
                "$set": {
                    "stock": modified
                }
            }
        stock.update_one({'productId': productId}, update)
        return f'Success remove stocks on index {index}'
    
async def removestocklisen(productId: str, index: int, isAll: bool):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stocklisen']
    data = stock.find_one({'productId': productId})
    if data is None:
        return f'Nothing to delete!'
    elif isAll:
        update = {
                "$set": {
                    "stock": []
                }
            }
        stock.update_one({'productId': productId}, update)
        return f'Success remove all stocks available!'
    else:
        data.get('stock').pop(index)
        modified = data.get('stock')
        update = {
                "$set": {
                    "stock": modified
                }
            }
        stock.update_one({'productId': productId}, update)
        return f'Success remove stocks on index {index}'
    
async def takestock(productId: str, amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stock']

    data = stock.find_one({'productId': productId})
    if data is None:
        return {'status': 400, 'message': 'Product ID not found!'}
    elif len(data.get('stock')) == 0:
        return {'status': 400, 'message': 'There is not available stock for that Product ID'}
    elif len(data.get('stock')) < amount:
        return {'status': 400, 'message': 'Insufficient amount of product'}
    elif len(data.get('stock')) >= amount:
        stockarray = data['stock']
        orderarray = stockarray[:amount]
        del stockarray[:amount]
        update = {
                "$set": {
                    "stock": stockarray
                }
            }
        stock.update_one({'productId': productId}, update)
        return {'status': 200, 'data': orderarray}
    else:
        return {'status': 400, 'message': 'Internal server error!'}
    
async def register(discordid: str, growid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']

    discordid = str(discordid)

    data = user.find_one({'discordid': discordid})
    queryfilter = {"growid": {"$regex": f"^{growid}$", "$options": "i"}}
    dupecheck = user.find_one(queryfilter)
    if data is None and dupecheck is None:
        query = {
            'database': 'User Customer Database',
            'discordid': discordid,
            'growid': growid,
            'worldlock': {'currency': 'wl', 'balance': 0},
            'rupiah': {'currency': 'rp', 'balance': 0},
            'totalspend': {'worldlock': 0, 'rupiah': 0}
        }
        user.insert_one(query)
        return f'Successfully register {growid}!'
    elif dupecheck is not None:
        return f'Grow ID is already registered!'
    else:
        update = {
                "$set": {
                    "growid": growid
                }
            }
        oldgrow = data.get('growid')
        user.update_one({'discordid': discordid}, update)
        return f'Successfully set from {oldgrow} to {growid}'
    
async def info(discordid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']

    data = user.find_one({'discordid': discordid})
    if data is None:
        return {'status': 400, 'message': 'Youre not registered yet!'}
    else:
        return {
            'status': 200,
            'message': 'Success fetch data!',
            'growid': data.get('growid'),
            'worldlock': data.get('worldlock'),
            'rupiah': data.get('rupiah'),
            'totalspend': data['totalspend']
        }
    
async def addtemplate():
    db = client[f'user_{client_data.SECRET_KEY}']
    assets = db[f'assets']

    data = assets.find_one({'database': 'User Assets'})
    if data is None:
        query = {
            'database': 'User Assets',
            'bannerurl': 'https://cdn.discordapp.com/attachments/1166767160878698628/1167104315261980743/standard.gif?ex=654ce998&is=653a7498&hm=a82e5dab07f1cd87999964cee579bec1e1b43c69257336ba15b7d3bdd0852bcb&',
            'sticker_1': '<a:Siren:1167137117453959270> ',
            'sticker_2': '<a:arrow4:1167148754772693012>',
            'sticker_3': '<:money1:1167148958053838949>',
            'sticker_4': '<:wl:1167146128622506134>',
            'sticker_5': '<a:darkbluecrown:1167155192773488710>',
            'sticket_6': '<a:GlowingPurpleLine:1176727267846672445>'
        }
        assets.insert_one(query)
        return f'Success added template to databases!'
    else:
        assets.delete_one({'database': 'User Assets'})
        query = {
            'database': 'User Assets',
            'bannerurl': 'https://cdn.discordapp.com/attachments/1166767160878698628/1167104315261980743/standard.gif?ex=654ce998&is=653a7498&hm=a82e5dab07f1cd87999964cee579bec1e1b43c69257336ba15b7d3bdd0852bcb&',
            'sticker_1': '<a:Siren:1167137117453959270> ',
            'sticker_2': '<a:arrow4:1167148754772693012>',
            'sticker_3': '<:money1:1167148958053838949>',
            'sticker_4': '<:wl:1167146128622506134>',
            'sticker_5': '<a:darkbluecrown:1167155192773488710>',
            'sticker_6': '<a:GlowingPurpleLine:1176727267846672445>'
        }
        assets.insert_one(query)
        return f'Success replace assets!'
    
async def changeassets(assetsid: str, value: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    assets = db[f'assets']

    data = assets.find_one({'database': 'User Assets'})
    if data is None:
        return f'Assets not found!'
    elif assetsid in ['bannerurl', 'sticker_1', 'sticker_2', 'sticker_3', 'sticker_4', 'sticker_5', 'sticker_6']:
        update = {
                "$set": {
                    assetsid: value
                }
            }
        assets.update_one({'database': 'User Assets'}, update)
        return f'Change template success!'
    else:
        return f'Assets ID is incorrect!'

async def getassets():
    db = client[f'user_{client_data.SECRET_KEY}']
    assets = db[f'assets']

    data = assets.find_one({'database': 'User Assets'})
    if data is None:
        return {'status': 400, 'message': 'Assets not found!'}
    else:
        return {
            'status': 200,
            'assets': {
                'bannerurl': data.get('bannerurl'),
                'sticker_1': data.get('sticker_1'),
                'sticker_2': data.get('sticker_2'),
                'sticker_3': data.get('sticker_3'),
                'sticker_4': data.get('sticker_4'),
                'sticker_5': data.get('sticker_5'),
                'sticker_6': data.get('sticker_6')
            }
        }
async def showassets():
    db = client[f'user_{client_data.SECRET_KEY}']
    assets = db[f'assets']

    data = assets.find_one({'database': 'User Assets'})
    if data is None:
        return {'status': 400, 'message': 'Nothing to show!'}
    else:
        return {'status': 200, 'assets': [
            {
                'code': 'bannerurl',
                'value': data.get('bannerurl')
            },
            {
                'code': 'sticker_1',
                'value': data.get('sticker_1')
            },
            {
                'code': 'sticker_2',
                'value': data.get('sticker_2')
            },
            {
                'code': 'sticker_3',
                'value': data.get('sticker_3')
            },
            {
                'code': 'sticker_4',
                'value': data.get('sticker_4')
            },
            {
                'code': 'sticker_5',
                'value': data.get('sticker_5')
            },
            {
                'code': 'sticker_6',
                'value': data.get('sticker_6')
            },
        ]}
    
async def give(discordid: str, type: str, amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']

    discordid = str(discordid)

    data =  user.find_one({'discordid': discordid})
    if data is None:
        return f'User not registered!'
    else:
        if type not in ['worldlock', 'rupiah']:
            return f'Type value must be "worldlock" or "rupiah"!'
        else:
            data[type]['balance'] = data[type]['balance'] + amount
            update = {
                "$set": {
                    type: data[type]
                }
            }
            user.update_one({'discordid': discordid}, update)
            if '-' in str(amount):
                return f'Success remove {str(amount).replace("-", "")} {type} from <@{discordid}>'
            else:
                return f'Success add {amount} {type} to <@{discordid}>'
            
async def givebal(growid: str, type: str, amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']

    growid = str(growid)
    queryfilter = {"growid": {"$regex": f"^{growid}$", "$options": "i"}}
    data =  user.find_one(queryfilter)
    if data is None:
        return {'status': 400, 'message': f'User {growid} not registered!', 'data': data}
    else:
        if type not in ['worldlock', 'rupiah']:
            return {'status': 400, 'message': 'Type value must be "worldlock" or "rupiah"!'}
        else:
            data[type]['balance'] = data[type]['balance'] + amount
            update = {
                "$set": {
                    type: data[type]
                }
            }
            user.update_one(queryfilter, update)
            if '-' in str(amount):
                return {'status': 200, 'message': f'Success remove {str(amount).replace("-", "")} {type} from <@{growid}>', 'data': data}
            else:
                return {'status': 200, 'message': f'Success add {amount} {type} to <@{growid}>', 'data': data}
            
async def setwebhook(webhookurl: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    webhook = db[f'webhook']

    data = webhook.find_one({'database': 'User Webhook'})
    if data is None:
        query = {
            'database': 'User Webhook',
            'webhookurl': webhookurl
        }
        webhook.insert_one(query)
        return f'Success set webhook to databases!'
    else:
        update = {
                "$set": {
                    'webhookurl': webhookurl
                }
            }
        webhook.update_one({'database': 'User Webhook'}, update)
        return f'Success set new webhook to databases!'
    
async def setwebhookid(webhookid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    webhook = db[f'webhookid']

    data = webhook.find_one({'database': 'User Webhook ID'})
    if data is None:
        query = {
            'database': 'User Webhook ID',
            'webhookid': webhookid
        }
        webhook.insert_one(query)
        return f'Success set webhook to databases!'
    else:
        update = {
                "$set": {
                    'webhookid': webhookid
                }
            }
        webhook.update_one({'database': 'User Webhook ID'}, update)
        return f'Success set new webhook to databases!'
    
async def getwebhookid():
    db = client[f'user_{client_data.SECRET_KEY}']
    webhook = db[f'webhookid']

    data = webhook.find_one({'database': 'User Webhook ID'})
    if data is None:
        return {'status': 400, 'message': 'Webhook ID not yet set!'}
    else:
        return {'status': 200, 'webhookid': data['webhookid']}
    
async def setdeposit(world: str, owner: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    deposit = db[f'deposit']

    data = deposit.find_one({'database': 'User Deposit'})
    if data is None:
        query = {
            'database': 'User Deposit',
            'world': world,
            'owner': owner
        }
        deposit.insert_one(query)
        return f'Success set deposit info to databases!'
    else:
        update = {
                "$set": {
                    'world': world,
                    'owner': owner
                }
            }
        deposit.update_one({'database': 'User Deposit'}, update)
        return f'Success set new deposit info to databases!'
    
async def getdeposit():
    db = client[f'user_{client_data.SECRET_KEY}']
    deposit = db[f'deposit']

    data = deposit.find_one({'database': 'User Deposit'})
    if data is None:
        return {'status': 400, 'message': 'Deposit info is not found!'}
    else:
        return {'status': 200, 'data': data}

async def checktotalstock(productid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stock']

    data = stock.find_one({'productId': productid})
    totalstock = 0
    if data is None:
        totalstock = 0
    else:
        totalstock = int(len(data.get('stock')))
    return totalstock

async def checktotalstocklisen():
    db = client[f'user_{client_data.SECRET_KEY}']
    stock = db[f'stocklisen']

    data = stock.find_one({'productId': 'botlisen'})
    totalstock = 0
    if data is None:
        pass
    else:
        totalstock = int(len(data.get('stock')))
    return totalstock

async def checkstocklisen():
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'productlisen']
    
    data = product.find_one({'database': 'User Product'})
    if data is None:
        return {'status': 400, 'message': 'Product is not found!'}
    else:
        array = data.get('productlist')
        for index, data in enumerate(array):
            stock = await checktotalstocklisen()
            data['totalstock'] = stock
        return {'status': 200, 'data': array}
        

async def checkstock():
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'product']

    productdata = product.find_one({'database': 'User Product'})
    if productdata is None:
        return {'status': 400, 'message': 'Product is not found!'}
    else:
        array = productdata.get('productlist')
        for index, data in enumerate(array):
            stock = await checktotalstock(data['productId'])
            data['totalstock'] = stock
        return {'status': 200, 'data': array}
    
async def isOrder(productid: str, amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'product']

    productdata = product.find_one({'database': 'User Product'})
    stockcheck = await checktotalstock(productid)
    if productdata is None:
        return {'status': 400, 'message': 'Product not been set!'}
    
    productcheck = await util_function.product_id_exists(productdata['productlist'], productid)
    if not productcheck:
        return {'status': 400, 'message': 'Product ID is invalid!'}
    
    if "-" in str(amount):
        return {'status': 400, 'message': 'Amount cannot contain "-"!'}
    elif amount == 0:
        return {'status': 400, 'message': 'Amount cannot be zero!'}
    elif stockcheck < amount:
        return {'status': 400, 'message': 'Insufficient stock!'}
    elif productdata is not None and stockcheck >= amount:
        array = productdata.get('productlist')
        for data in array:
            if data['productId'] == productid:
                object = data
                break
        return {'status': 200, 'message': 'Processing order..\n Bot will sent product via Direct Messages!', 'productdata': object}
    else:
        return {'status': 400, 'message': 'Internal server error!'}

async def isOrderlisen(productid: str, amount: int):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'productlisen']

    productdata = product.find_one({'database': 'User Product'})
    stockcheck = await checktotalstocklisen()
    if productdata is None:
        return {'status': 400, 'message': 'Product not been set!'}
    elif productdata is not None and stockcheck >= amount:
        array = productdata.get('productlist')
        count = 0
        price = 0
        
        for data in array:
            if data['productId'] == productid:
                count = count + 1
                object = data
                break
            else:
                pass
        if count == 0:
            return {'status': 400, 'message': 'Product code is invalid'}
        else:
            return {'status': 200, 'message': 'Processing order..\n Bot will sent product via Direct Messages!', 'productdata': object}
    else:
        return {'status': 400, 'message': 'Insufficient Stock!'}
        
async def setorderstate(state: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    states = db[f'states']

    data = states.find_one({'database': 'User State'})
    if data is None:
        query = {
            'database': 'User State',
            'state': state
        }
        states.insert_one(query)
        return f'Success create new state DB!'
    else:
        update = {
            "$set": {
                'state': state,
            }
        }
        states.update_one({'database': 'User State'}, update)
        return f'Success change state!'
    
async def checkstate():
    db = client[f'user_{client_data.SECRET_KEY}']
    states = db[f'states']

    data = states.find_one({'database': 'User State'})
    if data is None:
        return {'status': 400, 'message': 'State not found, please set it first!'}
    else:
        if data['state'] == "False":
            return {'status': 200, 'state': data['state']}
        else:
            return {'status': 400, 'message': 'Bot is still processing order, please wait for a moment!'}
        
async def setpresence(presence: str):
    db = client[f'user']
    selectpresence = db[f'data']

    data = selectpresence.find_one({'discordtoken': client_data.TOKEN})
    if data is None:
        return f'Data not found!'
    else:
        update = {
            "$set": {
                'presence': presence,
            }
        }
        selectpresence.update_one({'discordtoken': client_data.TOKEN}, update)
        return f'Success change presence, please restart your bot to apply!'

async def addstockbulkcmd(productId: str, productdetails: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'product']
    stock = db[f'stock']

    query = product.find_one({'database': 'User Product'})
    productCheck = 0 #if 0 then its False
    for data in query.get('productlist'):
        if data.get('productId') == productId:
            productCheck = productCheck + 1
            break
    
    if query is None:
        return 'Database not found!'
    elif productCheck == 0:
        return 'Product not existed in the databases!'
    else:

        sets_of_data = productdetails.split(',')
        array = []
        for data_set in sets_of_data:
            dictionary = {data_set}
            
            array.append(dictionary)

        stockQuery = stock.find_one({'productId': productId})
        if stockQuery is None:
            stockdata = {
                'database': 'User Stock',
                'productId': productId,
                'stock': sets_of_data
            }
            stock.insert_one(stockdata)
        else:
            stockArray = stockQuery.get('stock')
            stockArray.extend(sets_of_data)
            update = {
                "$set": {
                    "stock": stockArray
                }
            }
            stock.update_one({'productId': productId}, update)
        return 'Stock successfully added to the databases!'

async def addstockbulk(productId: str, productdetails: List[str]):
    db = client[f'user_{client_data.SECRET_KEY}']
    product = db[f'product']
    stock = db[f'stock']

    query = product.find_one({'database': 'User Product'})
    productCheck = 0 #if 0 then its False
    for data in query.get('productlist'):
        if data.get('productId') == productId:
            productCheck = productCheck + 1
            break
    
    if query is None:
        return 'Database not found!'
    elif productCheck == 0:
        return 'Product not existed in the databases!'
    else:

        sets_of_data = productdetails

        stockQuery = stock.find_one({'productId': productId})
        if stockQuery is None:
            stockdata = {
                'database': 'User Stock',
                'productId': productId,
                'stock': sets_of_data
            }
            stock.insert_one(stockdata)
        else:
            stockArray = stockQuery.get('stock')
            stockArray.extend(sets_of_data)
            update = {
                "$set": {
                    "stock": stockArray
                }
            }
            stock.update_one({'productId': productId}, update)
        return f'{len(sets_of_data)} Stock successfully added to the databases!'

async def setchannelhistory(channelid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    channel = db[f'channelhistory']

    data = channel.find_one({'database': 'User Channel History'})
    if data is None:
        query = {
            'database': 'User Channel History',
            'channelid': channelid
        }
        channel.insert_one(query)
        return f'Success set channel history to databases!'
    else:
        update = {
            "$set": {
                'channelid': channelid,
            }
        }
        channel.update_one({'database': 'User Channel History'}, update)
        return f'Success change channel history!'
    
async def getchannelhistory():
    db = client[f'user_{client_data.SECRET_KEY}']
    channel = db[f'channelhistory']

    data = channel.find_one({'database': 'User Channel History'})
    if data is None:
        return {'status': 400, 'message': 'Channel history not found!'}
    else:
        return {'status': 200, 'data': data['channelid']}
    
async def addlogs(logged):
    db = client[f'user_{client_data.SECRET_KEY}']
    logs = db[f'logs']

    data = logs.find_one({'database': 'User Logs'})
    if data is None:
        query = {
            'database': 'User Logs',
            'logs': [logged]
        }
        logs.insert_one(query)
        return f'Success create new logs DB!'
    else:
        logsArray = data.get('logs')
        logsArray.append(logged)
        update = {
            "$set": {
                'logs': logsArray,
            }
        }
        logs.update_one({'database': 'User Logs'}, update)
        return f'Success add logs!'
    
async def showlogs():
    db = client[f'user_{client_data.SECRET_KEY}']
    logs = db[f'logs']

    data = logs.find_one({'database': 'User Logs'})
    if data is None:
        return {'status': 400, 'message': 'Logs not found!'}
    else:
        return {'status': 200, 'data': data['logs']}
    
async def deletelogs():
    db = client[f'user_{client_data.SECRET_KEY}']
    logs = db[f'logs']

    data = logs.find_one({'database': 'User Logs'})
    if data is None:
        return {'status': 400, 'message': 'Logs not found!'}
    else:
        update = {
            "$set": {
                'logs': [],
            }
        }
        logs.update_one({'database': 'User Logs'}, update)
        return {'status': 200, 'message': 'Success delete logs!'}

async def claim(secretkey: str, license: str):
    db = client[f'user']
    bot = db[f'data']

    data = bot.find_one({'secretkey': secretkey})
    if data is None:
        return {'status': 400, 'message': 'Secret key not found!'}
    else:
        if license in data['license'] and data['status'] == False:
            data['license'].remove(license)
            expdate = util_function.getonemonth()
            update = {
                "$set": {
                    "license": data['license'],
                    "expdate": expdate,
                    "status": True
                }
            }
            bot.update_one({'secretkey': secretkey}, update)
            return {'status': 200, 'message': f'Success, bot will expired on {expdate}'}
        elif license in data['license'] and data['status'] == True:
            data['license'].remove(license)
            expdate = util_function.addonemonth(data['expdate'])
            update = {
                "$set": {
                    "license": data['license'],
                    "expdate": expdate,
                    "status": True
                }
            }
            bot.update_one({'secretkey': secretkey}, update)
            return {'status': 200, 'message': f'Success, bot will expired on {expdate}'}
        else:
            return {'status': 400, 'message': f'License is not valid!'}
        
async def registerbot(discordtoken: str, discordid: str, license, secretkey: str):
    db = client[f'user']
    user = db[f'data']

    data = user.find_one({'discordtoken': discordtoken})
    secretcheck = user.find_one({'secretkey': secretkey})
    if data is None and secretcheck is None:
        query = {
            'database': 'User Data',
            'discordid': discordid,
            'discordtoken': discordtoken,
            'secretkey': secretkey,
            'presence': 'Hello World!',
            'license': [license],
            'expdate': '',
            'status': False
        }
        user.insert_one(query)
        return {'status': 200, 'message': 'Success, check direct message to get your details!'}
    elif data is not None and data['secretkey'] == secretkey:
        oldarray = data['license']
        newarray = oldarray.append(license)
        update = {
                "$set": {
                    "license": data['license']
                }
            }
        user.update_one({'discordtoken': discordtoken}, update)
        return {'status': 200, 'message': 'Success, check direct message to get your details!'}
    elif data is not None and data['secretkey'] != secretkey:
        return {'status': 400, 'message': 'Wrong secretkey for that Token!'}
    elif secretcheck is not None:
        return {'status': 400, 'message': 'Secretkey already exist, use another password!'}

async def checksecret(SECRET_KEY: str):
    db = client["user"]
    collection = db["data"]

    data = collection.count_documents({'secretkey': SECRET_KEY})
    if data == 1:
        return {'status': 200, 'message': 'Authorized!'}
    elif data == 0:
        return {'status': 400, 'message': 'Unauthorized!'}
    else:
        return {'status': 400, 'message': 'Error occured!'}
    
async def addip(ip: str):
    db = client[f'user']
    listipwhitelist = db[f'ip']

    filter ={'database': 'IP Whitelist'}

    data = listipwhitelist.find_one(filter)
    if data is None:
        query = {
            'database': 'IP Whitelist',
            'ip': [ip]
        }
        listipwhitelist.insert_one(query)
        return 'Success add IP to whitelist!'
    else:
        oldarray = data['ip']
        newarray = oldarray.append(ip)
        update = {
                "$set": {
                    "ip": data['ip']
                }
            }
        listipwhitelist.update_one(filter, update)
        return 'Success add new IP to whitelist!'
    
async def addadmin(discordid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    admin = db[f'admin']

    filter = {'database': 'User Admin'}

    data = admin.find_one(filter)
    if data is None:
        query = {
            'database': 'User Admin',
            'admin': [discordid]
        }
        admin.insert_one(query)
        return f'Success add admin to the databases!'
    elif discordid in data['admin']:
        return f'Target Discord ID is alread an admin!'
    else:
        data['admin'].append(discordid)
        update = {
                "$set": {
                    "admin": data['admin']
                }
            }
        admin.update_one(filter, update)
        return f'Success add admin to the databases!'
    
async def removeadmin(discordid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    admin = db[f'admin']

    filter = {'database': 'User Admin'}

    data = admin.find_one(filter)
    if data is None or discordid not in data['admin']:
        return f'Admin list does not found!'
    elif discordid in data['admin']:
        data['admin'].remove(discordid)
        update = {
                "$set": {
                    "admin": data['admin']
                }
            }
        admin.update_one(filter, update)
        return f'Success remove admin from the databases!'
    
async def getadmin():
    db = client[f'user_{client_data.SECRET_KEY}']
    admin = db[f'admin']

    filter = {'database': 'User Admin'}

    data = admin.find_one(filter)
    if data is None:
        return {'status': 400, 'message': 'Admin query is not found!', 'data': []}
    else:
        return {'status': 200, 'message': 'Success', 'data': data['admin']}
    
async def setup():
    db = client[f'user_{client_data.SECRET_KEY}']

    setuplist = [
        {'name': 'assets', 'isSetup': False, 'command': '/addassets', 'filter': {'database': 'User Assets'}},
        {'name': 'channelhistory', 'isSetup': False, 'command': '/setchannelhistory', 'filter': {'database': 'User Channel History'}},
        {'name': 'deposit', 'isSetup': False, 'command': '/setdeposit', 'filter': {'database': 'User Deposit'}},
        {'name': 'product', 'isSetup': False, 'command': '/setproduct', 'filter': {'database': 'User Product'}},
        {'name': 'states', 'isSetup': False, 'command': '/setorderstate', 'filter': {'database': 'User State'}},
        {'name': 'webhookid', 'isSetup': False, 'command': '/setwebhookid', 'filter': {'database': 'User Webhook ID'}}
    ]

    for index, setup in enumerate(setuplist):
        usersetup = db[setup['name']]
        data = usersetup.find_one(setup['filter'])
        if data is not None:
            setuplist[index]['isSetup'] = True
        else:
            pass
    return setuplist

async def addtotalbuy():
    db = client[f'user_{client_data.SECRET_KEY}']
    buy = db[f'totalbuy']

    filter = {'database': 'User Total Buy'}
    data = buy.find_one(filter)
    if data is None:
        total = 1
        query = {
            'database': 'User Total Buy',
            'total': total
        }
        buy.insert_one(query)
        return total
    else:
        newtotal = data['total'] + 1
        update = {
                "$set": {
                    "total": newtotal
                }
            }
        buy.update_one(filter, update)
        return newtotal
    
async def upgrade():
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']

    data = user.find({})
    if data is None:
        return {'status': 400, 'message': 'Data does not exist!'}
    else:
        user.update_many({}, {"$set": {"totalspend": {'worldlock': 0, 'rupiah': 0}}})
        return {'status': 200, 'message': 'Success update database!'}

async def addtotalspend(discordid: str, amount: float):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']
    
    filter = {'discordid': str(discordid)}
    data = user.find_one(filter)
    update = {
        "$set": {
            "totalspend": {'worldlock': data['totalspend']['worldlock'] + float(amount), 'rupiah': data['rupiah']}
        }
    }
    user.update_one(filter, update)

async def gettopten():
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'growid']

    data = user.find_one({'database': 'User Customer Database'})
    if data is None:
        return {'status': 400, 'message': 'No user found in the databases!'}
    try:
        result = user.aggregate([
            {"$sort": {"totalspend.worldlock": -1}},  # Sort by totalspend.worldlock descending
            {"$limit": 10}  # Limit the results to 10 documents
        ])
        arr =  []
        for document in result:
            arr.append(document)
        return {'status': 200, 'message': 'Success fetching top ten data!', 'data': arr}
    except:
        return {'status': 400, 'message': 'Error on fetching data, please try /upgrade and try again!'}

async def addmuterole(roleid: str, guildid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'muterole']

    filter = {'database': 'User Muted Role'}

    data = user.find_one(filter)

    if data is None:
        query = {
            'database': 'User Muted Role',
            'guildid': str(guildid),
            'roleid': str(roleid)
        }

        user.insert_one(query)
        return {'status': 200, 'message': 'Success set mute role!'}
    else:
        update = {
            "$set": {
                "roleid": roleid
            }
        }
        user.update_one(filter, update)
        return {'status': 200, 'message': 'Success set new mute role!'}
    
async def addmuteuser(discordid: str, expired: str, reason: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'muteuser']

    data = user.find_one({'discordid': discordid})
    if data is not None:
        return {'status': 400, 'message': 'User already muted!'}

    query = {
        'database': 'User Muted',
        'discordid': discordid,
        'expired': expired,
        'reason': reason
    }

    user.insert_one(query)
    return {'status': 200, 'message': 'Success add muted user!'}

async def removemuteuser(discordid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'muteuser']

    user.find_one_and_delete({'discordid': discordid})
    return f'Success'

async def getmuterole():
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'muterole']

    data = user.find_one({'database': 'User Muted Role'})
    if data is None:
        return{'status': 400, 'message': 'Muted role not been set!'}
    
    return {'status': 200, 'message': 'Muted role is ready!', 'data': data['roleid'], 'guild': data['guildid']}

async def getmuteuser(discordid: str):
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'muteuser']
    filter = {'discordid': str(discordid)}
    data = user.find_one(filter)
    if data is None:
        return{'status': 400, 'message': 'User does not exist!'}
    
    return {'status': 200, 'message': 'User exist!', 'data': data}

async def getmuteuserall():
    db = client[f'user_{client_data.SECRET_KEY}']
    user = db[f'muteuser']

    data = user.find({})
    arr = []
    for datas in data:
        arr.append(datas)
    return arr