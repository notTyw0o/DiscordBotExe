import discord
import mongo
import discordembed
import util_function
import client_data
import asyncio

bot = discord.Bot()

class Register(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Grow ID"))

    async def callback(self, interaction: discord.Interaction):
        request = await mongo.register(interaction.user.id, self.children[0].value)
        await interaction.send_message(request, ephemeral=True)

class Order(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        

        self.add_item(discord.ui.InputText(label="Product Code"))
        self.add_item(discord.ui.InputText(label="Amount"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=await discordembed.textembed(f'Processing order..'), ephemeral=True)
        try:
            int(self.children[1].value)
        except:
            embed = await discordembed.textembed('Amount must be an integer!')
            return await interaction.followup.send(embed=embed, ephemeral=True)
        
        isOrder = await mongo.isOrder(self.children[0].value, int(self.children[1].value))
        isState = await mongo.checkstate()
        userBalance = await mongo.info(str(interaction.user.id))
        try:
            userBalance = userBalance['worldlock']['balance']
            totalprice = int(self.children[1].value) * int(isOrder['productdata']['productPrice'])
            isOrder['productdata']['amount'] = int(self.children[1].value)
            isOrder['productdata']['totalprice'] = totalprice
        except:
            embed = await discordembed.textembed(isOrder['message'])
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        if isOrder['status'] == 200 and isState['status'] == 200 and userBalance >= totalprice:
            await mongo.setorderstate('True')
            request = await mongo.takestock(self.children[0].value, int(self.children[1].value))
            asyncio.create_task(mongo.setorderstate('False'))
            if request['status'] == 200:
                removebalance = await mongo.give(str(interaction.user.id), 'worldlock', -totalprice)
                if "Success" in removebalance:
                    user = interaction.user
                    guild = interaction.guild
                    assets = await mongo.getassets()
                    async def processorder():
                        msg = ""
                        for text in request['data']:
                            msg += text + "\n"
                        try:
                            footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                        except:
                            footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                        embed = await discordembed.orderembed(isOrder['productdata'], assets['assets'], footer, str(interaction.user.id))
                        files = await util_function.write_text_file(f"== YOUR ORDER DETAILS ==\n{msg}", str(interaction.user.id))
                        file = discord.File(f'/home/ubuntu/txtfiles/{str(interaction.user.id)}.txt')
                        await user.send(file=file)
                        await user.send(embed=embed)
                        await util_function.delete_text_file(str(interaction.user.id))
                        asyncio.create_task(mongo.addtotalspend(str(interaction.user.id), float(isOrder['productdata']['totalprice'])))
                        userlogs = {
                            'discordid': str(interaction.user.id), 
                            'productname': isOrder['productdata']['productName'],
                            'amount': str(isOrder['productdata']['amount']),
                            'totalprice': str(isOrder['productdata']['totalprice']),
                            'product': request['data']
                            }
                        asyncio.create_task(mongo.addlogs(userlogs))
                        channelid = await mongo.getchannelhistory()
                        if channelid['status'] == 200:
                            channel = guild.get_channel(int(channelid['data']))
                            asyncio.create_task(channel.send(embed=embed))
                    
                    
                    asyncio.create_task(mongo.convertadminstock(request['data']))
                    async def addrole():
                        try:
                            role = discord.utils.get(guild.roles, id=int(isOrder['productdata']['roleId']))
                            member = guild.get_member(user.id)
                            await member.add_roles(role)
                            arrow = assets['assets']['sticker_2']
                            responseembed = await discordembed.secondtextembed(f'{arrow} **Added new role : {role.name} ✅**\n{arrow} **Status : Success ✅**\n**Please check Direct Messages!**', 'Order Success')
                            asyncio.create_task(interaction.followup.send(embed=responseembed, ephemeral=True))
                        except Exception as e:
                            arrow = assets['assets']['sticker_2']
                            responseembed = await discordembed.secondtextembed(f'{arrow} **Added new role : ❌**\n{arrow} **Status : Success ✅**\n**Please check Direct Messages!**', 'Order Success')
                            asyncio.create_task(interaction.followup.send(embed=responseembed, ephemeral=True))
                        
                    asyncio.create_task(processorder())
                    asyncio.create_task(addrole())
                    
                else:
                    await mongo.setorderstate('False')
                    await interaction.followup.send(removebalance, ephemeral=True)
            else:
                await mongo.setorderstate('False')
                await interaction.followup.send(request['message'], ephemeral=True)
        elif isOrder['status'] == 400:
            await interaction.followup.send(isOrder['message'], ephemeral=True)
        elif isState['status'] == 400:
            await interaction.followup.send(isState['message'], ephemeral=True)
        elif userBalance < totalprice:
            await interaction.followup.send(f'Insufficient balance!', ephemeral=True)     

