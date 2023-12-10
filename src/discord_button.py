import discord
import discord_modal
import asyncio
import mongo
import discordembed

bot = discord.Bot()

class OrderButton(discord.ui.View):
    @discord.ui.button(label="Order here!", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(discord_modal.Order(bot, title='Order Products!'))

class Verification(discord.ui.View):
    def __init__(self, role_id, **kwargs):
        super().__init__(**kwargs)
        self.role_id = role_id

    @discord.ui.button(label="Click me!", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        user = interaction.user
        guild = interaction.guild
        assets = await mongo.getassets()
        try:
            role = discord.utils.get(guild.roles, id=int(self.role_id))
            member = guild.get_member(user.id)
            await member.add_roles(role)
            arrow = assets['assets']['sticker_2']
            responseembed = await discordembed.secondtextembed(f'{arrow} **Added new role : {role.name} ✅**', 'Verification Success')
            asyncio.create_task(interaction.response.send_message(embed=responseembed, ephemeral=True))
        except Exception as e:
            arrow = assets['assets']['sticker_2']
            responseembed = await discordembed.textembed(f'Verification failed!')
            asyncio.create_task(interaction.response.send_message(embed=responseembed, ephemeral=True))