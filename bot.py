
# coding=utf8

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from subprocess import call


load_dotenv('.env')

await_response = []
watch_list = []
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    
    with open('watch_channels.txt') as file:
        for line in file:
            watch_list.append(line)
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
    if(ctx.guild != None):
        if(ctx.channel.name in watch_list):
            await ctx.send('{0}ms'.format(round(client.latency * 1000)))

@client.command(pass_context=True)
async def server(ctx, arg):
    if(ctx.guild != None):
        if(ctx.channel.name in watch_list):
            if(arg == "on"):
                await ctx.send('Turning on the server')
                rc = call("./turn_on.sh")
            elif(arg == "off"):
                await ctx.send('Turning off the server')
                rc = call("./turn_off.sh")
            else:
                await ctx.send('Invalid argument following .server')

@client.command()
async def assign_channel(ctx):
    if(ctx.guild != None):
        mod = discord.utils.get(ctx.guild.roles, id=int(os.getenv('ROLE_ID')))
        if(mod in ctx.author.roles):
            watch_list.append(ctx.channel.name)
            with open("watch_channels.txt", "a") as myfile:
                myfile.write("{0}\n".format(ctx.channel.name))
            await ctx.send("Text-channel {0} is now added to the watch list".format(ctx.channel.name))
        else:
            await ctx.send("You don't have permission to do this command")

#@client.command(pass_context=True)
#async def help(ctx):
#    await ctx.send('The commands available are:')
#    await ctx.send('```* help - With all the commands\n* turnOn - To turn on the valheim server')

client.run(os.getenv('DISCORD_TOKEN'))
