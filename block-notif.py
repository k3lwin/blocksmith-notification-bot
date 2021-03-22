#!/usr/bin/env python3

import requests
import json

import time
from datetime import datetime

import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed

load_dotenv()
WEBHOOK = os.getenv('DISCORD_WEBHOOK')

#Save previous block info
try:
	response = requests.get("https://rvn.bsmith.io/api/poolStats")
except:
	print("Unable to get pool stats:", sys.exc_info()[0])

prev_block = json.loads(response.text)['minedBlocks'][0]

#Wakeup notification
webhook = DiscordWebhook(url=WEBHOOK)
description="Last block mined on " + datetime.fromtimestamp(prev_block['timestamp']).strftime("%Y-%m-%d %H:%M:%S") + "\n" + str(datetime.utcnow() - datetime.fromtimestamp(prev_block['timestamp'])) + " ago"
embed = DiscordEmbed(title='Bot online', description=description, color='03b2f8')
webhook.add_embed(embed)
webhook.execute()

#Checking for new blocks every 10 seconds
while True:
	try:
		response = requests.get("https://rvn.bsmith.io/api/poolStats")
	except ConnectionError as e:
		print("Connection error, will try again", e)

	last_block = json.loads(response.text)['minedBlocks'][0]

	if last_block == prev_block:
		continue
	else:
		embed = DiscordEmbed(title='New block mined!', color='f0a800')
		embed.add_embed_field(name="Number", value=last_block['number'], inline=False)
		embed.add_embed_field(name="Miner", value=last_block['miner'], inline=False)
		embed.add_embed_field(name="Date", value=datetime.fromtimestamp(last_block['timestamp']).strftime("%Y-%m-%d %H:%M:%S"))
		prev_block = last_block

		webhook.add_embed(embed)
		webhook.execute()

	time.sleep(10)