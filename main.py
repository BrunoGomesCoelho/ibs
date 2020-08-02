import os
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync
import urlextract


if __name__ == "__main__":
    # Load confs
    load_dotenv(override=True, verbose=True)

    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    session_name = os.getenv("SESSION_NAME")
    bs_peer = os.getenv("BS_PEER")

    print("Using", api_id, api_hash)
    print("Session name", session_name)
    print("BS peer is", bs_peer)

    with TelegramClient(session_name, api_id, api_hash) as client:
        client.send_message(bs_peer, 'International BS online!')
        extractor = urlextract.URLExtract()
        queue_peer = set()
        queue_curr = set()

        # TODO: contains URL (auto push)
        @client.on(events.NewMessage())
        async def auto_push(event):
            print("Received", event.message.text)

            if extractor.has_urls(event.message.text):
                print("Yo! You sent a link")
                sender = await event.message.get_sender()
                if sender.username == bs_peer:
                    queue_curr.add(event.message.id)
                else:
                    queue_peer.add(event.message.id)
            print("Queue current user:", queue_curr)
            print("Queue peer user:", queue_peer)

        # TODO: replied to pushed (auto pop)
        # @client.on(events.NewMessage(pattern='(?i).*Hello'))
        # async def handler(event):
        #     await event.reply('Hey!')

        # TODO: contains pop (manual pop)
        # @client.on(events.NewMessage(pattern='(?i).*Hello'))
        # async def handler(event):
        #     await event.reply('Hey!')

        client.run_until_disconnected()

    # messages = client.get_messages('cruzao')
    # messages[0].download_media()
