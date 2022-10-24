import os
import json
import time
import math
import discord
import aiohttp
import asyncio

HDL_ENDPOINT = os.getenv('HDL_ENDPOINT')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
MESSAGE_ID = int(os.getenv('MESSAGE_ID'))

client = discord.Client(intents=discord.Intents.default())

async def update():
    print('update!')
    async with aiohttp.ClientSession() as session:
        worlds_r = await session.get(HDL_ENDPOINT + '/api/worlds')
        worlds_j = await worlds_r.json()
        worlds = map(lambda x: x['name'], worlds_j['result'])
        newmsg = f'**SESSION LIST** (edited: <t:{math.floor(time.time())}:R> )' + '\n'
        for i, world in enumerate(worlds):
            actual = ''
            while actual != world:
                status_r = await session.get(HDL_ENDPOINT + f'/api/status?arg={i}')
                status_j = await status_r.json()
                status = status_j['result']
                actual = status['name']
                print('retry!')
                await asyncio.sleep(3)
            newmsg += f'> {status["name"]} ({status["present_users"]}/{status["max_users"]})' + '\n'
            newmsg += 'users: ' + ' '.join(status["users"]) + '\n'
            newmsg += '\n'

    channel = client.get_channel(CHANNEL_ID)
    message = await channel.fetch_message(MESSAGE_ID)
    await message.edit(content=newmsg)

@client.event
async def on_ready():
    while True:
        await update()
        await asyncio.sleep(60)

client.run(BOT_TOKEN)

