import util_function
import asyncio
import discord
import mongo
import discordembed
import client_data
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def create_footer(ctx):
    try:
        footer = {'name': ctx.author.name,'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
    except:
        footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
    return footer

async def check_muted(guild, discordid, roleid):
    mutedid = int(roleid)  # Replace this with your muted role ID
    muted_role = guild.get_role(int(mutedid))
    member = guild.get_member(discordid)

    if muted_role in member.roles:
        return True
    else:
        return False

async def mute_task(guild, member_id, duration):
    duration = int(duration) * 3600
    await asyncio.sleep(duration)
    muteuser = await mongo.getmuteuser(member_id)
    muterole = await mongo.getmuterole()
    if muteuser['status'] == 400 or muterole['status'] == 400:
        return

    muted_role = guild.get_role(int(muterole['data']))
    member = guild.get_member(int(member_id))
    if member:
        checkmute = await check_muted(guild, int(member_id), muterole['data'])
        if not checkmute:
            return
        await member.remove_roles(muted_role)
        await mongo.removemuteuser(str(member_id))
        # You might want to change this to use `guild.send` instead of `ctx.send`
        await member.send(embed=await discordembed.textembed(f"You have been unmuted from {guild.name}."))

async def fetch_mute_timers(guild):
    mute_timers = await mongo.getmuteuserall()
    for timer in mute_timers:
        member_id = int(timer['discordid'])
        print(timer["expired"])
        duration = int(await util_function.seconds_until_future_time(str(timer["expired"])))

        if duration == 0:
            await mongo.removemuteuser(timer['discordid'])
            continue

        member = discord.utils.get(guild.members, id=member_id)

        if member:
            asyncio.create_task(mute_task(guild, member_id, duration))
        else:
            await mongo.removemuteuser(timer['discordid'])

async def send_message_to_channel(channelid: str, guild: str):

    channel = guild.get_channel(int(channelid))

    if not channel:
        owner = discord.utils.get(guild.members, id=int(client_data.OWNER_ID))
        await owner.send(embed=await discordembed.textembed(f'Error, cannot get Channel ID!'))
        return
    
    request = await mongo.getstockadmin()
    assets = await mongo.getassets()
    assets = assets['assets']
    arrow = assets.get('sticker_2')
    msg = ""
    for message in request:
        msg += f'{arrow} <@{message["admin"]}> - Instock: {len(message["instock"])} - Sold: {len(message["sold"])}\n'

    msg = msg.rstrip('\n')

    await channel.send(embed=await discordembed.secondtextembed(msg,'Admin Stock List'))