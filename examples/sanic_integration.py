"""This example showcases how to use rebootpy with the asynchronous
web framework sanic.
Must be using Sanic Version 21.6.2 or lower
"""

import rebootpy
import json
import os
import sanic

from rebootpy.ext import commands


filename = 'device_auths.json'
description = 'My awesome fortnite bot / sanic app!'


def get_device_auth_details():
    with open(filename, 'r') as fp:
        return json.load(fp)


device_auths = get_device_auth_details()
bot = commands.Bot(
    command_prefix='!',
    auth=rebootpy.DeviceAuth(
        **device_auths
    )
)

sanic_app = sanic.Sanic(__name__)
host = "0.0.0.0"
port = 80
server = None

@bot.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@app.main_process_start
async def main_start(*_):
    print(f"Sanic Server Ready {host}:{port}")

@sanic_app.route('/friends')
async def get_friends_handler(request):
    friends = [friend.id for friend in bot.friends]
    return sanic.response.json(friends)

@bot.event
async def event_ready():
    global server

    print(f'Bot ready as {bot.user.display_name} ({bot.user.id}).')

    server = await sanic_app.create_server(
        port=port, host=host, return_asyncio_server=True
    )

    await server.startup()
    await server.serve_forever()


@bot.event
async def event_before_close():
    global server

    if server:
        await server.close()


@bot.event
async def event_friend_request(request):
    await request.accept()


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


bot.run()
