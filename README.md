# International BullShit

Telegram link management "bot" inside DM chats

## Getting Started

First of all you'll need a [Telegram API token](https://docs.telethon.dev/en/latest/basic/signing-in.html). Once you have that, create a file named `.env` following the example on [`sample_dotenv`](https://github.com/BrunoGomesCoelho/ibs/blob/master/sample_dotenv):

```
API_ID=????
API_HASH=????????????????????????????????
SESSION_NAME=session_name
TITLE=InternationalBullShit
BS_PEER=????
DEBUG=0
```

Replace the `?`s with your information. `BS_PEER` is the Telegram nickname of the person you wish to use `ibs` with (without the leading *@*). If you'd like to see debugging logs, set `DEBUG` to `1` instead of `0`.

After that, install the requirement libraries
```sh
$ python3 -m pip install -r requirements.txt
``` 
And run the bot 
```sh
$ python3 main.py
``` 

The first time you use the program, you might need to confirm a code on your phone.

**WARNING**: The Telegram API should not be used for spamming or harassement. Doing so could permanently ban your account.

## How it works

Telegram Bots cannot be added to private chats (i.e. direact messages). `ibs`, however, acts like a daemon that uses your Telegram API key to manage your messages with your `BS_PEER`. 

Any link you send to the other person gets added to their queue. Any link the person sends you gets added to your queue. Both of you can then pop that a specific video from the queue by replying to the original message, or pop the oldest not yet watched video with `/pop`.

## Contributing

Feel free to open an issue if you found a bug or would like to request a feature.

## Authors

Originally coded by @[BrunoGomesCoelho](https://github.com/BrunoGomesCoelho) and @[gmelodie](https://github.com/gmelodie) in a coffee-filled afternoon.
