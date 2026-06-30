# Building the bot: DM a user when they leave a voice channel

This bot does one thing: the moment a user disconnects from a voice channel
in a server it's in, it sends them a DM. This guide walks through building
it from nothing — Discord Developer Portal setup, local environment,
the code, and how to run/host it.

## 1. Prerequisites

- **Python 3.10+** installed (`python3 --version` to check).
- **pip** (ships with Python).
- **Node.js** — already used in this repo for git hooks (Husky) and commit
  message linting (Commitlint). You don't need it to *run* the bot, only if
  you're committing to this repo.
- A **Discord account**.
- A **Discord server you manage** (or can create one for free) to invite
  and test the bot in.

## 2. Discord Developer Portal setup

1. Go to <https://discord.com/developers/applications> and click
   **New Application**. Give it a name (this is just the app's name, not
   necessarily what shows in Discord — you can set that under "Bot").
2. In the left sidebar, click **Bot**.
3. Click **Reset Token** (or **Copy** if a token is already shown) and copy
   the token somewhere safe. **Treat this like a password** — anyone with
   it can control your bot. You'll paste it into `.env` in a moment.
4. **About "Privileged Gateway Intents":** this bot only needs to know when
   someone's voice state changes, which is a *normal* (non-privileged)
   intent. Discord only gates three intents behind the "Privileged" toggle
   on this page: **Presence Intent**, **Server Members Intent**, and
   **Message Content Intent** — none of which this bot needs. You can leave
   all three off. (Optional: turning on **Server Members Intent** makes
   Discord's member cache more complete, which can make `member.send(...)`
   slightly more reliable in large servers — but it isn't required for this
   feature to work.)
5. In the left sidebar, click **OAuth2 → URL Generator**.
   - Under **Scopes**, check `bot`.
   - Under **Bot Permissions**, you don't need to check anything — DMing a
     user doesn't require a server permission. (If you later want the bot
     to also post in a channel, you'd add `Send Messages` here.)
   - Copy the generated URL at the bottom, paste it into your browser,
     pick your test server, and authorize it.
6. Confirm the bot now shows up (as offline, until you run it) in your test
   server's member list.

## 3. Environment setup

From the repo root:

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install runtime + dev dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Create your local secrets file
cp .env.example .env
```

Open `.env` and replace the placeholder with the token you copied in step 2:

```
DISCORD_TOKEN=the-token-you-copied
```

`.env` is already in `.gitignore` — it will never be committed.

## 4. The code

`bot.py` (repo root):

```python
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
            await member.send(
                'عن أبي هريرة رضي الله عنه، قال رسول الله ﷺ: «مَنْ جَلَسَ فِي مَجْلِسٍ فَكَثُرَ فِيهِ لَغَطُهُ، فَقَالَ قَبْلَ أَنْ يَقُومَ مِنْ مَجْلِسِهِ ذَلِكَ: سُبْحَانَكَ اللَّهُمَّ وَبِحَمْدِكَ، أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا أَنْتَ، أَسْتَغْفِرُكَ وَأَتُوبُ إِلَيْكَ.. إِلَّا غُفِرَ لَهُ مَا كَانَ فِي مَجْلِسِهِ ذَلِكَ»'
            )
        except discord.Forbidden:
            # The member has DMs from server members disabled, or has
            # blocked the bot. Log it and move on instead of crashing.
            logger.warning('Could not DM %s: DMs are closed.', member)


client.run(TOKEN)
```

**Walkthrough:**

- `load_dotenv()` + `os.getenv('DISCORD_TOKEN')` pulls the token out of
  `.env` so it's never hardcoded in the source.
- `discord.Intents.default()` gives a sane baseline set of intents;
  `intents.voice_states = True` adds the one this feature actually needs.
- `on_ready` just confirms the bot connected successfully — useful for
  debugging.
- `on_voice_state_update(member, before, after)` fires on *every* voice
  change for *every* member: joining, leaving, moving channels, muting,
  deafening, etc. `before` and `after` are snapshots of that member's voice
  state immediately before and after the change, so comparing
  `before.channel` and `after.channel` is how you tell what kind of change
  happened.
- The `if` guard is the entire "did they leave" logic: they were in a
  channel, now they're in none. (If you also want a DM when someone
  *switches* channels, change the condition to
  `before.channel != after.channel and after.channel is None` — same thing,
  written for clarity — or drop the `is None` checks entirely to fire on
  every join/leave/move.)
- `member.send(...)` opens (or reuses) a DM channel with that user and
  sends the message — here, the dhikr said upon leaving a gathering
  ("kaffarat al-majlis"), fitting for a "Majlis Thikr" bot. Python source
  files are UTF-8 by default and Discord fully supports Unicode, so Arabic
  text needs no special handling. It's wrapped in `try/except discord.Forbidden` because
  Discord raises that error if the user's privacy settings block DMs from
  the bot — without the `try/except`, that would crash the bot's event
  loop on the very first user who has DMs locked down.

## 5. Execution and hosting

**Run it locally** (with the venv activated and `.env` filled in):

```bash
python bot.py
```

You should see `Logged in as <YourBotName>#0000` in the terminal. Join a
voice channel in your test server, then leave it — you should get a DM
within a second or two.

**Hosting it 24/7:** running it in a terminal only works while your machine
is on and the process is alive. For always-on hosting, two common options:

- **A small VPS** (e.g. a $5/mo DigitalOcean/Linode droplet) — clone the
  repo, repeat the environment setup, and run the bot under a process
  supervisor so it restarts automatically on crash or reboot. Either a
  `systemd` service, or `pm2` (`pm2 start bot.py --interpreter python3`)
  if you'd rather not write a systemd unit file.
- **A PaaS with native Python support** (Railway, Render, Fly.io, etc.) —
  push the repo, set `DISCORD_TOKEN` as an environment variable in their
  dashboard (never commit it), and point the start command at
  `python bot.py`. These platforms handle restarts/uptime for you.

Either way: the bot token goes in the host's environment variable
configuration, never in a committed file.
