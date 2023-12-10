import discord
import mongo
import client_data
import discord_modal as modal
import discordembed
import discord_button
import util_function

bot = discord.Bot(intents=discord.Intents.all())


class MainView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Hello, choose command here!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="📝| Register Grow ID",
                description="Register your Grow ID!"
            ),
            discord.SelectOption(
                label="👤| User Information",
                description="Get your user information!"
            ),
            discord.SelectOption(
                label="💸| Deposit Information",
                description="Get deposit information!"
            ),
            discord.SelectOption(
                label="🛒| Order Product",
                description="Order an product!"
            ),
        ]
    )
    async def select_callback(self, select, interaction):
        isActive = await mongo.checkOwner(client_data.SECRET_KEY)
        parts = select.values[0].split("|")
        selectedvalues = parts[1].strip()
        if isActive['status'] == 200:
            if selectedvalues == "None":
                await interaction.response.send_message('Nothing!', ephemeral=True)
            elif selectedvalues == "Register Grow ID":
                await interaction.response.send_modal(modal.Register(title=select.values[0]))
            elif selectedvalues == "User Information":
                userid = str(interaction.user.id)
                request = await mongo.info(userid)
                template = await mongo.getassets()
                if request.get('status') == 200 and template.get('status') == 200:
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.infoembed(request, template.get('assets'), footer)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif request.get('status') == 400:
                    await interaction.response.send_message(request.get('message'), ephemeral=True)
                elif template.get('status') == 400:
                    await interaction.response.send_message(template.get('message'), ephemeral=True)
            elif selectedvalues == "Deposit Information":
                request = await mongo.getdeposit()
                template = await mongo.getassets()
                if request.get('status') == 200 and template.get('status') == 200:
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.depositembed(request, template.get('assets'), footer)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif request.get('status') == 400:
                    await interaction.response.send_message(request.get('message'), ephemeral=True)
                elif template.get('status') == 400:
                    await interaction.response.send_message(template.get('message'), ephemeral=True)
            elif selectedvalues == "Order Product":
                await interaction.response.send_modal(modal.Order(bot, title=select.values[0]))
            else:
                await interaction.response.send_message('Not yet set!', ephemeral=True)
        else:
            await interaction.response.send_message(isActive['message'], ephemeral=True)

class MainViewEmail(discord.ui.View):
    @discord.ui.select(
        placeholder = "Hello, choose command here!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="📝| Register Grow ID",
                description="Register your Grow ID!"
            ),
            discord.SelectOption(
                label="👤| User Information",
                description="Get your user information!"
            ),
            discord.SelectOption(
                label="💸| Deposit Information",
                description="Get deposit information!"
            ),
            discord.SelectOption(
                label="🛒| Order Product",
                description="Order an product!"
            ),
        ]
    )
    async def select_callback(self, select, interaction):
        isActive = await mongo.checkOwner(client_data.SECRET_KEY)
        parts = select.values[0].split("|")
        selectedvalues = parts[1].strip()
        if isActive['status'] == 200:
            if selectedvalues == "None":
                await interaction.response.send_message('Nothing!', ephemeral=True)
            elif selectedvalues == "Register Grow ID":
                await interaction.response.send_modal(modal.Register(title=select.values[0]))
            elif selectedvalues == "User Information":
                userid = str(interaction.user.id)
                request = await mongo.info(userid)
                template = await mongo.getassets()
                if request.get('status') == 200 and template.get('status') == 200:
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.infoembed(request, template.get('assets'), footer)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif request.get('status') == 400:
                    await interaction.response.send_message(request.get('message'), ephemeral=True)
                elif template.get('status') == 400:
                    await interaction.response.send_message(template.get('message'), ephemeral=True)
            elif selectedvalues == "Deposit Information":
                request = await mongo.getdeposit()
                template = await mongo.getassets()
                if request.get('status') == 200 and template.get('status') == 200:
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.depositembed(request, template.get('assets'), footer)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif request.get('status') == 400:
                    await interaction.response.send_message(request.get('message'), ephemeral=True)
                elif template.get('status') == 400:
                    await interaction.response.send_message(template.get('message'), ephemeral=True)
            elif selectedvalues == "Order Product":
                await interaction.response.send_modal(modal.OrderEmail(bot, title=select.values[0]))
            else:
                await interaction.response.send_message('Not yet set!', ephemeral=True)
        else:
            await interaction.response.send_message(isActive['message'], ephemeral=True)

class License(discord.ui.View):
    @discord.ui.select(
        placeholder = "Hello, choose command here!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="None",
                description=""
            ),
            discord.SelectOption(
                label="Stock License",
                description="Check stock of available license!"
            ),
            discord.SelectOption(
                label="Order Store Bot License",
                description="Order license!"
            ),
            discord.SelectOption(
                label="Claim License",
                description="Claim your license here!"
            ),
        ]
    )
    async def select_callback(self, select, interaction):
        selectedvalues = select.values[0]
        if selectedvalues == "Order Store Bot License":
            await interaction.response.send_modal(modal.RegisterLicense(title=select.values[0]))
        elif selectedvalues == "Stock License":
            checkstock = await mongo.checkstocklisen()
            try:
                footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
            except:
                footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
            embed = await discordembed.checkstocklisen(checkstock, footer)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif selectedvalues == "Claim License":
            await interaction.response.send_modal(modal.Claim(title=select.values[0]))
        elif selectedvalues == "None":
            await interaction.response.send_message('Nothing', ephemeral=True)

class Controller(discord.ui.View):
    @discord.ui.select(
        placeholder = "Hello, choose command here!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="None",
                description=""
            ),
            discord.SelectOption(
                label="Start Bot",
                description="Start running your bot here!"
            ),
            discord.SelectOption(
                label="Off Bot",
                description="Turning off your bot here!"
            ),
            discord.SelectOption(
                label="Restart Bot",
                description="Restart your bot here!"
            ),
        ]
    )
    async def select_callback(self, select, interaction):
        selectedvalues = select.values[0]
        if selectedvalues == "Start Bot":
            await interaction.response.send_modal(modal.Start(title=select.values[0]))
        elif selectedvalues == "Off Bot":
            await interaction.response.send_modal(modal.Off(title=select.values[0]))
        elif selectedvalues == "Restart Bot":
            await interaction.response.send_modal(modal.Restart(title=select.values[0]))
        elif selectedvalues == "None":
            await interaction.response.send_message('Nothing', ephemeral=True)


