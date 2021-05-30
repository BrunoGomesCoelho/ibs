import os
import json
import logging
from pathlib import Path
from collections import OrderedDict

import urlextract
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync


backup = {
    "curr": [],
    "peer": [],
}


def write_backup():
    """TODO: document
    """
    with open("backup.json", "w") as f:
        json.dump(backup, f)


async def auto_push(message, sender, extractor, bs_peer_username):
    if not extractor.has_urls(message.text):
        return

    urls = extractor.find_urls(message.text)
    logging.debug(f"{sender.username} sent a link")

    if sender.username == bs_peer_username:
        backup["curr"] += urls
        queue_curr[message.id] = message
    else:
        backup["peer"] += urls
        queue_peer[message.id] = message

    # newline

    write_backup()  # readibility 100


async def auto_pop(message, sender, bs_peer_username):
    if message.text.startswith("/ignore") or message.text.startswith("/repop"):
        logging.debug("Ignoring pop of {msg}")
        return

    older_msg = await message.get_reply_message()
    older_id = older_msg.id
    if sender.username == bs_peer_username and older_id in queue_peer:
        msg = queue_peer.pop(older_id)
        logging.debug("Popping from reply msg {msg}")
    if sender.username != bs_peer_username and older_id in queue_curr:
        msg = queue_curr.pop(older_id)
        logging.debug("Popping from reply msg {msg}")


if __name__ == "__main__":
    # Load confs
    load_dotenv(override=True, verbose=True)
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    session_name = os.getenv("SESSION_NAME")
    bs_peer_username = os.getenv("BS_PEER")
    debug = bool(int(os.getenv("DEBUG")))

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info(f"Using, {api_id}, {api_hash}")
    logging.info(f"Session name, {session_name}")
    logging.info(f"BS peer is, {bs_peer_username}")

    queue_peer = OrderedDict()
    queue_curr = OrderedDict()
    extractor = urlextract.URLExtract()

    with TelegramClient(session_name, api_id, api_hash) as client:
        bs_peer_id = client.get_peer_id(bs_peer_username)
        client.send_message(bs_peer_username , 'International BS online!')

        @client.on(events.NewMessage(chats=[bs_peer_id]))
        async def auto_push_pop(event):
            sender = await event.message.get_sender()
            if event.message.is_reply:
                await auto_pop(event.message, sender, bs_peer_username)
            if extractor.has_urls(event.message.text):
                await auto_push(event.message, sender, extractor, bs_peer_username)

            logging.debug(f"Queue current user:, {queue_curr}")
            logging.debug(f"Queue peer user:, {queue_peer}")

        @client.on(events.NewMessage(pattern='(?i)\/pop$'))
        async def manual_pop(event):
            sender = await event.message.get_sender()
            msg = None
            queue = queue_peer if sender.username == bs_peer_username else queue_curr
            if queue:
                _, msg = queue.popitem(last=False)
                await msg.reply("Popping this")
            else:
                backup_key = "peer" if sender.username == bs_peer_username else "curr"
                backup[backup_key] = []
                write_backup()  # writes backup, function is called
                await event.reply("No bullshit")

        client.run_until_disconnected()

