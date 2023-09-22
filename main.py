import os
import json
import logging
from pathlib import Path
from collections import OrderedDict
import asyncio

import urlextract
from dotenv import load_dotenv
from pyrogram import Client, idle, filters


# Load confs
load_dotenv(override=True, verbose=True)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
BS_PEER_USERNAME = os.getenv("BS_PEER")
MY_USERNAME = os.getenv("MY_USERNAME")
DEBUG = bool(int(os.getenv("DEBUG")))
# enable logs
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logging.info(f"Using, {API_ID}, {API_HASH}")
logging.info(f"Session name, {SESSION_NAME}")
logging.info(f"BS peer is, {BS_PEER_USERNAME}")
logging.info(f"Your telegram username is: {MY_USERNAME}")

# get data from backup if exists
if os.path.isfile("backup.json"):
    logging.info(f"backup found, loading")
    with open("backup.json", "r") as f:
        backup = json.load(f)

queue_peer = OrderedDict()
queue_curr = OrderedDict()
extractor = urlextract.URLExtract()

# Pattern to match the command /pop
POP_MSG_FILTER   = filters.regex(r'(?i)\/pop$')
PEER_USER_FILTER = filters.user(BS_PEER_USERNAME)
MY_USER_FILTER   = filters.user(MY_USERNAME)


backup = {
    "curr": [],
    "peer": [],
}

client = Client(MY_USERNAME, API_ID, API_HASH)


def write_backup():
    """TODO: document
    """
    with open("backup.json", "w") as f:
        json.dump(backup, f)


async def auto_push(message, sender, extractor):
    if not extractor.has_urls(message.text):
        return

    urls = extractor.find_urls(message.text)
    logging.debug(f"{sender.username} sent a link")

    if sender.username == BS_PEER_USERNAME:
        backup["curr"] += urls
        queue_curr[message.id] = message
    else:
        backup["peer"] += urls
        queue_peer[message.id] = message

    # newline

    write_backup()  # readibility 100


async def auto_pop(message, sender):
    if message.text.startswith("/ignore") or message.text.startswith("/repop"):
        logging.debug("Ignoring pop of {msg}")
        return

    older_msg = message.reply_to_message
    older_id = older_msg.id
    if sender.username == BS_PEER_USERNAME and older_id in queue_peer:
        msg = queue_peer.pop(older_id)
        logging.debug("Popping from reply msg {msg}")
    if sender.username != BS_PEER_USERNAME and older_id in queue_curr:
        msg = queue_curr.pop(older_id)
        logging.debug("Popping from reply msg {msg}")


# TODO: change to chat filter
@client.on_message((PEER_USER_FILTER | MY_USER_FILTER) & POP_MSG_FILTER)
async def manual_pop(client, message):
    sender = message.from_user
    logging.debug(f"Received pop from {sender.username}")
    msg = None
    queue = queue_peer if sender.username == BS_PEER_USERNAME else queue_curr
    if queue:
        _, msg = queue.popitem(last=False)
        await msg.reply_text("Popping this", quote=True)
    else:
        backup_key = "peer" if sender.username == BS_PEER_USERNAME else "curr"
        backup[backup_key] = []
        write_backup()  # writes backup, function is called
        await message.reply_text("No bullshit", quote=True)


# TODO: change to chat filter
@client.on_message(PEER_USER_FILTER | MY_USER_FILTER)
async def auto_push_pop(client, message):
    sender = message.from_user
    if message.reply_to_message:
        await auto_pop(message, sender)
    if extractor.has_urls(message.text):
        await auto_push(message, sender, extractor)

    logging.debug(f"Queue current user:, {queue_curr}")
    logging.debug(f"Queue peer user:, {queue_peer}")



async def main():
    await client.start()
    await client.send_message(BS_PEER_USERNAME , 'International BS 2.0 online!')
    await idle()
    await client.stop()

client.run(main())
