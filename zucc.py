import discord
import asyncio
import logging
import json
import sys
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                    handlers=[logging.FileHandler("zucc.log"), logging.StreamHandler(stream=sys.stdout)])
log = logging.getLogger('zucc')

if discord.version_info.major < 1:
    print("This version of discord.py is not the rewrite! Run `pip install -r requirements.txt` to fix this.")
    sys.exit(1)

if not os.path.isfile("config.json"):
    with open("config.json", 'w') as f:
        json.dump({
            "token": "put token here",
            "megazucc": 1,
            "megazucc_guild": 0,

        }, f, indent=2)
    print("A new config.json has been written.\n"
          "Set megazucc to 1 to enable startup server dumping, and set megazucc_guild to the target guild's id,"
          " then restart this script.", file=sys.stderr)
    sys.exit(1)



with open("config.json") as f:
    config = json.load(f)

megazucc = bool(config["megazucc"])
megazucc_guild_id = int(config["megazucc_guild"])


def g(thing):
    return thing.guild.id == megazucc_guild_id

config['megazucc'] = 0
with open("config.json", 'w') as f:
    json.dump(config, f, indent=2)

zucc = discord.Client()


def log_msg(msg: discord.Message):
    a = {
        'channel': str(msg.channel),
        'author': msg.author.display_name,
        'content': msg.content,
        }
    if msg.embeds:
        a['embeds'] = [e.to_dict() for e in msg.embeds]

    if msg.attachments:
        a['attachments'] = []
        for at in msg.attachments:
            a['attachments'].append(at.url)
            # await at.save(f"{at.id}_{at.filename}")

    a['meta'] = {
        'id': msg.id,
        'timestamp': msg.created_at.isoformat(),
        'authordata': (msg.author.id, str(msg.author), msg.author.display_name),
        'channel_id': msg.channel.id
    }

    log.info(json.dumps(a))


@zucc.event
async def on_ready():
    global megazucc
    log.info(f"Logged in as {zucc.user}")
    await zucc.change_presence(status=discord.Status.invisible)

    if megazucc:
        log.info("Performing megazucc")
        megazucc = False
        guild = zucc.get_guild(megazucc_guild_id)
        for c in guild.text_channels:
            try:
                count = 0
                exc_count = 0
                async for msg in c.history(limit=None, reverse=True):
                    try:
                        log_msg(msg)
                        count += 1
                        if count % 50 == 0:
                            await asyncio.sleep(2)
                    except Exception:
                        exc_count += 1
                        if exc_count > 50: break
            except Exception:
                pass
        await asyncio.sleep(4)

        log.info("Done with megazucc")


@zucc.event
async def on_message(msg : discord.Message):
    if not g(msg): return
    log_msg(msg)


@zucc.event
async def on_message_delete(msg : discord.Message):
    if not g(msg): return
    log.info(json.dumps({"action": "deleted", "id": msg.id}))


@zucc.event
async def on_message_edit(before : discord.Message, after : discord.Message):
    if not g(after): return
    log.info(json.dumps({"action": "edited", "id": before.id}))
    log_msg(after)


@zucc.event
async def on_member_join(member : discord.Member):
    if not g(member): return

    log.info(json.dumps({
        'action': "joined server",
        'authordata': (member.id, str(member), member.display_name)
    }))

@zucc.event
async def on_member_remove(member : discord.Member):
    if not g(member): return
    log.info(json.dumps({
        'action': "left server",
        'authordata': (member.id, str(member), member.display_name)
    }))

zucc.run(config["token"], bot=True)
