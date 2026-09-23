import logging
import os
import random

import discord
from dotenv import load_dotenv

from phrases import BATYA_PHRASES

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
TARGET_USER_ID = int(os.getenv("TARGET_USER_ID", "498130253038747648"))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", "1283109126305611799"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("batya")


class BatyaBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.none()
        intents.guilds = True
        intents.guild_messages = True
        intents.message_content = True
        super().__init__(intents=intents, allowed_mentions=discord.AllowedMentions.none())

    async def on_ready(self):
        log.info(
            "Connected as %s; target_user=%s; target_channel=%s; phrases=%s",
            self.user,
            TARGET_USER_ID,
            TARGET_CHANNEL_ID,
            len(BATYA_PHRASES),
        )

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id != TARGET_USER_ID or message.channel.id != TARGET_CHANNEL_ID:
            return

        phrase = random.choice(list(BATYA_PHRASES.values()))
        await message.channel.send(phrase)


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Set DISCORD_TOKEN in environment or .env")
    BatyaBot().run(TOKEN)
