import logging
import os
import random

import discord
from dotenv import load_dotenv

from phrases import BATYA_PHRASES, SHE_PHRASES

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
TARGET_USER_ID = int(os.getenv("TARGET_USER_ID", "498130253038747648"))
SECOND_USER_ID = int(os.getenv("SECOND_USER_ID", "437335754780442646"))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", "1283109126305611799"))
NOZAR_MIN_MESSAGES = int(os.getenv("NOZAR_MIN_MESSAGES", "10"))
NOZAR_MAX_MESSAGES = int(os.getenv("NOZAR_MAX_MESSAGES", "50"))
SECOND_USER_MESSAGE_INTERVAL = int(os.getenv("SECOND_USER_MESSAGE_INTERVAL", "3"))
ONLINE_PHRASE = os.getenv("ONLINE_PHRASE", "пошла нахуй отсюда")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("batya")


class BatyaBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.none()
        intents.guilds = True
        intents.guild_messages = True
        intents.message_content = True
        intents.presences = True
        super().__init__(intents=intents, allowed_mentions=discord.AllowedMentions.none())
        self.nozar_message_count = 0
        self.nozar_next_reply_at = self.next_nozar_threshold()
        self.second_user_message_count = 0

    def next_nozar_threshold(self):
        return random.randint(NOZAR_MIN_MESSAGES, NOZAR_MAX_MESSAGES)

    async def on_ready(self):
        log.info(
            "Connected as %s; target_user=%s; second_user=%s; target_channel=%s; phrases=%s; she_phrases=%s",
            self.user,
            TARGET_USER_ID,
            SECOND_USER_ID,
            TARGET_CHANNEL_ID,
            len(BATYA_PHRASES),
            len(SHE_PHRASES),
        )

    async def send_to_target_channel(self, guild, text):
        channel = guild.get_channel(TARGET_CHANNEL_ID) if guild else None
        if channel is None:
            channel = self.get_channel(TARGET_CHANNEL_ID)
        if channel is not None:
            await channel.send(text)

    async def on_presence_update(self, before, after):
        if after.bot or after.id != SECOND_USER_ID:
            return
        if before.status == discord.Status.offline and after.status != discord.Status.offline:
            await self.send_to_target_channel(after.guild, ONLINE_PHRASE)

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.id != TARGET_CHANNEL_ID:
            return

        if message.author.id == TARGET_USER_ID:
            self.nozar_message_count += 1
            if self.nozar_message_count >= self.nozar_next_reply_at:
                self.nozar_message_count = 0
                self.nozar_next_reply_at = self.next_nozar_threshold()
                await message.channel.send(random.choice(BATYA_PHRASES))
            return

        if message.author.id == SECOND_USER_ID:
            self.second_user_message_count += 1
            if self.second_user_message_count % SECOND_USER_MESSAGE_INTERVAL == 0:
                await message.channel.send(random.choice(SHE_PHRASES))


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Set DISCORD_TOKEN in environment or .env")
    BatyaBot().run(TOKEN)
