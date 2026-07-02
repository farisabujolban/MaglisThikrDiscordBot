import logging
import os

import discord
from dotenv import load_dotenv

# Load DISCORD_TOKEN from a local .env file (see .env.example).
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot')

# Intents tell Discord which events we want to receive. `voice_states` is
# what lets us see voiceStateUpdate-style events at all; it is NOT a
# privileged intent (those are members, presences, and message content),
# so nothing needs to be toggled on in the Developer Portal for this to work.
intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info('Logged in as %s', client.user)


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # "Left a voice channel" = was in a channel before, and is in no channel
    # now. This guard excludes moving between two channels, which also
    # fires this event but isn't a "leave".
    if before.channel is not None and after.channel is None:
        try:
            # Discord has no markup for arbitrary hex text colors; an ansi
            # code block is the only way to render colored inline text, and
            # its palette is a fixed set of 8 terminal colors. Bold green
            # ([1;32m) is the closest available match to #4DFFBC.
            dua = 'سُبْحَانَكَ اللَّهُمَّ وَبِحَمْدِكَ، أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا أَنْتَ، أَسْتَغْفِرُكَ وَأَتُوبُ إِلَيْكَ'
            colored_dua = f'```ansi\n[1;32m{dua}[0m\n```'
            await member.send(
                f'عن أبي هريرة رضي الله عنه، قال رسول الله ﷺ: «مَنْ جَلَسَ فِي مَجْلِسٍ فَكَثُرَ فِيهِ لَغَطُهُ، '
                f'فَقَالَ قَبْلَ أَنْ يَقُومَ مِنْ مَجْلِسِهِ ذَلِكَ: {colored_dua}.. '
                'إِلَّا غُفِرَ لَهُ مَا كَانَ فِي مَجْلِسِهِ ذَلِكَ»'
            )
        except discord.Forbidden:
            # The member has DMs from server members disabled, or has
            # blocked the bot. Log it and move on instead of crashing.
            logger.warning('Could not DM %s: DMs are closed.', member)


client.run(TOKEN)
