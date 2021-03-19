
# coding=utf8

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from subprocess import call
import time
from datetime import datetime
import asyncio 


load_dotenv('.env')

await_response = []
watch_list = []
client = commands.Bot(command_prefix = '.')

server_time = 0
server_status = False

async def time_loop():
	while True:
		global server_time
		global server_status
		guild = client.get_guild(int(os.getenv('GUILD_ID')))
		channel1 = guild.get_channel(int(os.getenv('CHANNEL_ID')))
		#channel1 = discord.utils.get(guild.text_channels, name="valheim-boys")
		messages = await channel1.history(limit=200).flatten()
		now = datetime.now()
		for msg in messages:
			delta_time = now.timestamp() - msg.created_at.timestamp()
			if(delta_time > (90*60) and not msg.pinned):
				await msg.delete()

		if(server_time < now.timestamp() and server_status):
			print("Server ran out of time")
			rc = call("./turn_off.sh")
			server_status = False

		await asyncio.sleep(10)


@client.event
async def on_ready():
	with open('watch_channels.txt') as file:
		for line in file:
			watch_list.append(line[:-1])
	print('Bot started')
	await time_loop()
	




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
async def change(ctx,arg):
	if(ctx.guild != None):
		if(ctx.channel.name in watch_list):
			global server_time
			if(server_time != 0 and isinstance(int(arg),int)):
				server_time += int(arg)*60*60
				await ctx.send('Added {0} hours to server uptime'.format(arg))

@client.command(pass_context=True)
async def server(ctx, arg):
	
	if(ctx.guild != None):
		if(ctx.channel.name in watch_list):
			global server_time
			if(arg == "on"):
				now = datetime.now()
				server_time = now.timestamp() + (60*60*2)
				await ctx.send('Turning on the server')
				await ctx.send('Server will be turned off automatically in 2 hours if .change isnt used')
				rc = call("./turn_on.sh")
				global server_status
				server_status = True

			elif(arg == "off"):
				server_time = 0
				await ctx.send('Turning off the server')
			else:
				await ctx.send('Invalid argument following .server')

@client.command()
async def assign_channel(ctx):
	if(ctx.guild != None):
		mod = discord.utils.get(ctx.guild.roles, id=int(os.getenv('ROLE_ID')))
		if(mod in ctx.author.roles):
			
			if(ctx.channel.name in watch_list):
				await ctx.send("This channel is already in watched list")
			else:
				watch_list.append(ctx.channel.name)
				with open("watch_channels.txt", "a") as myfile:
					myfile.write("{0}\n".format(ctx.channel.name))
				await ctx.send("Text-channel {0} is now added to the watch list".format(ctx.channel.name))
		else:
			await ctx.send("You don't have permission to do this command")

client.run(os.getenv('DISCORD_TOKEN'))
