# IBS - International BullShit

IBS is a Telegram "bot" to help any two friends manage all the ~~research~~ YouTube links they send each other.

It works by automatically adding any link you send to the other person's list; They can then pop that specific video from the list by replying to the original message, or pop the oldest not yet watched video with the command ```/pop```.


## Getting Started

Due to how Telegram Bots are limited in non group chats, it is implemented as a constantly running program that uses the users API keys to manage the messages. For setting up valid credentials, view the relevant [telethon docs](https://docs.telethon.dev/en/latest/basic/signing-in.html) and then setup your own .env file, following the example of ```sample_dotenv```. The settings you need to change are API_ID, API_HASH and BS_PEER, this last one being the nickname of the friend you would like to to (ie, @myName).

**WARNING**: Your telegram api should not be used for spamming or harassement and a invalid use might permanently ban your account.

After that, run ```python3 -m pip install -r requirements.txt``` to install all the libraries and ```python3 main.py``` to run. The first time you use the program, you might need to confirm a code on your phone.

## Contributing

Feel free to open a issue and contribute with the code.

## Authors

Originally coded by @[BrunoGomesCoelho](https://github.com/BrunoGomesCoelho) and @[GMelodie](https://github.com/gmelodie) in a coffee filled afternon.
