# blocksmith-notification-bot
Simple bot notifying Discord users of Blocksmith pool about new mined blocks. 

Requirements (install with pip):
- discord_webhook
- python-dotenv
- requests

Place your webhook URL in `.env` file like this:

```
DISCORD_WEBHOOK="<webhook URL>"
```
If you want a message with previous block date on every bot startup, in `.env` add:
```
BANNER=1
```
