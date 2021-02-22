
# coding=utf8

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from subprocess import call


load_dotenv('.env')

await_response = []
players = []
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot started')

@client.event
async def on_member_join(member):
    channel = await member.create_dm()
    await channel.send('Hola!')
    await_response.append(member)

@client.event
async def on_message(message):
    if message.guild == None:
        if message.author in await_response:
            await message.channel.send('Dont message me freak')
    await client.process_commands(message)

@client.command()
async def ping(ctx):
    await ctx.send('{0}ms'.format(round(client.latency * 1000)))

@client.command(pass_context=True)
async def turnOn(ctx):
    await ctx.send('Turning on the server')
    rc = call("./turn_on.sh")

@client.command(pass_context=True)
async def turnOff(ctx):
    await ctx.send('Turning off the server')
    rc = call("./turn_off.sh")


client.run(os.getenv('DISCORD_TOKEN'))
