# dm_helper.py
# Helpers for sending DMs
import discord


async def can_dm_user(user: discord.User) -> bool:
    ch = user.dm_channel
    if ch is None:
        ch = await user.create_dm()

    try:
        await ch.send()
    except discord.Forbidden:
        return False
    except discord.HTTPException:
        return True
