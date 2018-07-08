# Zucc
a Discord bot that z u c c s tasty data bits from a guild/server

## Requirements:
* Python 3.6+ (this is important because 3.6+ perserves dict insertion order)
* the discord.py rewrite (installable with `pip install -r requirements.txt`)

## Installation:
1. clone the git repo
2. install the discord.py rewrite, either in a virtualenv or through `pip install -r requirements.txt`
3. run `zucc.py` once to generate `config.json`
4. edit config.json as advised by the zucc.py script. An example final config looks something like this, but without the comments as they make invalid JSON:

```javascript
{
  "token": "[bot token]",
  "megazucc": 1, // always without quotes, set to zero if you do not want the bot to dump all message in all channels on startup. 
  "megazucc_guild": 0 // the id of the guild to dump everything on.
}
```

5. Run the bot, and watch it all be dumped to `zucc.log`.

## Considerations for operation:
If the `megazucc` option is set to 1, the zucc will iterate over every channel in the set `megazucc_guild` and dump every message from oldest to newest to `zucc.log`. 
This is intended to be a one-time process, and the zucc script will automatically disable the `megazucc` option to 0 in the config.

Server owners may need to inform users that they are recording data for archival or moderation purposes (or otherwise) in order to be ToS compliant.

One could hypothetically change the `bot=True` on the last line of `zucc.py` to `bot=False` and set `token` in `config.json` to a user account's token, however,
that would be considered a ToS breaking selfbot and is not a supported mode of operation. Such accounts may be subject to banishment and deletion by Discord. 
