#!/usr/bin/env python3

import requests
import json
import sys

import time
from datetime import datetime

import os
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed

def chop_ms(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)

load_dotenv()
WEBHOOK = os.getenv('DISCORD_WEBHOOK')
BANNER = os.getenv("BANNER", 'False').lower() in ['true', '1']

#Save previous block info
try:
	response = requests.get("https://rvn.bsmith.io/api/poolStats")
except requests.exceptions.RequestException as e:
	print("Unable to get pool stats:", sys.exc_info()[0])

prev_block = json.loads(response.text)['minedBlocks'][0]

#Wakeup notification
if BANNER == True:
	webhook = DiscordWebhook(url=WEBHOOK)
	description="Last block mined on " + datetime.utcfromtimestamp(prev_block['timestamp']).strftime("%Y-%m-%d %H:%M:%S") + " UTC \n" + str(datetime.utcnow() - datetime.utcfromtimestamp(prev_block['timestamp'])).split(".")[0] + " ago"
	embed = DiscordEmbed(title='Bot online', description=description, color='03b2f8')
	webhook.add_embed(embed)
	webhook.execute()
else:
	print("Banner off, prev block date", datetime.utcfromtimestamp(prev_block['timestamp']).strftime("%Y-%m-%d %H:%M:%S"))

#Checking for new blocks every 10 seconds
while True:
	try:
		response = requests.get("https://rvn.bsmith.io/api/poolStats")
		last_block = json.loads(response.text)['minedBlocks'][0]
	except requests.exceptions.RequestException as e:
		print("Connection error, will try again", e)
		time.sleep(1)

	if last_block['number'] == prev_block['number']:
		continue
	else:
		webhook = DiscordWebhook(url=WEBHOOK)
		embed = DiscordEmbed(title='New block mined!', color='f0a800')
		embed.add_embed_field(name="Number", value=last_block['number'], inline=False)
		embed.add_embed_field(name="Miner", value="`" + last_block['miner'] + "`", inline=False)
		embed.add_embed_field(name="Effort", value=last_block['effort'] + "%", inline=False)
		embed.add_embed_field(name="Date", value=datetime.utcfromtimestamp(last_block['timestamp']).strftime("%Y-%m-%d %H:%M:%S") + " UTC")
		webhook.add_embed(embed)
		webhook.execute()

		prev_block = last_block


	time.sleep(10)