import discord
import util_function
import mongo

async def infoembed(field, assets, footer):
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')
    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )
    embed.add_field(
        name=f"{siren} **User Information** {siren}",
        value=f"{crown} **Registered GrowID** :\n{arrow} {field.get('growid')}\n{crown} **Your balance :** \n{arrow} {await util_function.format_number(field.get('worldlock').get('balance'))} {worldlock}\n{assets.get('sticker_2')} {util_function.rupiah_format(field.get('rupiah').get('balance'))} {money}\n\n{crown} **Total Spend:**\n{arrow} {field['totalspend']['worldlock']} {worldlock}", inline=True
        )
    embed.set_thumbnail(url=footer.get('avatar'))
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed

async def showembed(listassets, assets, footer):
    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )

    for data in listassets:
        embed.add_field(
            name=f"**Assets Code: \n{data.get('code')}**",
            value=f"{data.get('value')}", inline=False
            )
    embed.set_image(url=assets.get('bannerurl'))
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed

async def depositembed(listassets, assets, footer):
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')
    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )
    embed.add_field(
        name=f"{siren} **Deposit Information** {siren}",
        value=f"{crown} **Deposit World :** \n{arrow} {listassets.get('data').get('world')}\n{crown} **Owner :** \n{arrow} {listassets.get('data').get('owner')}", inline=True
        )
    embed.set_image(url=assets.get('bannerurl'))
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed

async def checkstockembed(listassets, assets, footer):
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')
    line = assets.get('sticker_6')
    line = f'{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}'
    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )
    for data in listassets['data']:
        embed.add_field(
        name=f"{crown} **{data['productName']}**",
        value=f"{arrow} Code : {data['productId']}\n{arrow} Price : {await util_function.format_number(data['productPrice'])} {worldlock}\n{arrow} Stock : {data['totalstock']}\n {line}", inline=False)
    embed.add_field(name=f"{siren} **HOW TO BUY** {siren}", value=f"{arrow} **Click this Menu below**\n{arrow} **Click on 'Register Grow ID'**\n{arrow} **Click on 'Deposit Information'**\n{arrow} **Go drop Worldlock to the deposit world**\n{arrow} **Click 'User Information' to check balance**\n{arrow} **Then click on 'Order Product'**")
    embed.set_image(url=assets.get('bannerurl'))
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed

async def orderembed(product, assets, footer, custdiscordid):
    totalbuy = await mongo.addtotalbuy()
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')
    productName = product['productName']
    amount = product['amount']
    totalprice = product['totalprice']
    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )
    embed.add_field(
        name=f"{siren} **Order Success #{totalbuy}** {siren}",
        value=f"{arrow} **Buyer : <@{custdiscordid}>**\n{arrow} **Product : {productName}**\n{arrow} **Total : {amount}**\n{arrow} **Total Price : {await util_function.format_number(totalprice)} {worldlock}**\n {siren} **Note : Give reps for warranty!**", inline=True
        )
    embed.set_image(url=assets.get('bannerurl'))
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed

async def deploy(footer):
    assets = await mongo.getassets()
    assets = assets['assets']
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')
    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )
    embed.add_field(
        name=f"{siren} **User Command** {siren}",
        value=f""
        )
    embed.set_image(url=assets.get('bannerurl'))
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed

async def deploylicense(footer):
    assets = await mongo.getassets()
    assets = assets['assets']
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')
    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )
    embed.add_field(
        name=f"{siren} **User Command** {siren}",
        value=f""
        )
    embed.set_image(url=assets.get('bannerurl'))
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed

async def checkstocklisen(listassets, footer):
    assets = await mongo.getassets()
    
    assets = assets['assets']
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')

    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )

    for data in listassets['data']:
        embed.add_field(
        name=f"{crown} **{data['productName']}**",
        value=f"{arrow} Code : {data['productId']}\n{arrow} Price : {data['productPrice']} {worldlock}\n{arrow} Stock : {data['totalstock']}", inline=True)
    
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed

async def textembed(text: str):
    assets = await mongo.getassets()
    
    assets = assets['assets']
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')

    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )

    embed.add_field(
        name=f"{siren} {text}",
        value=f""
        )
    return embed

async def secondtextembed(text: str, title: str):
    assets = await mongo.getassets()
    
    assets = assets['assets']
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')

    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )

    embed.add_field(
        name=f"{siren} **{title}** {siren}",
        value=f"{text}"
        )
    return embed