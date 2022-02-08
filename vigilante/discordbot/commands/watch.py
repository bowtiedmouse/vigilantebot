from discord.ext import commands
from discord.commands import permissions
from discord.commands import slash_command
import discord

from discordbot.settings import GUILD_IDS, ADMIN_ROLES


class WatchCommands(commands.Cog):
    """
    Commands for set alerts and get updates on targets.
    """

    def __init__(self, _bot):
        self.bot = _bot

    # TODO: /watch: Starts the watch turn on on targets. Will report regularly.
    @slash_command(name='watch', guild_ids=GUILD_IDS)
    async def watch(self, ctx: discord.ApplicationContext):
        await ctx.respond("Start watch command!")

    # TODO: /stop: @only_admin Will stop the watching activity.
    @slash_command(name='stop', guild_ids=GUILD_IDS, default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    @permissions.is_owner()
    async def stop_watch(self, ctx: discord.ApplicationContext):
        await ctx.respond("Stop watch command!")

    # TODO: /report_target <address or alias>: Reports updates for that target, tagging the caller.
    #  Will use autocomplete.

    # TODO: /subscribe <address or alias> <token>: Tags or DM the caller when the target has
    #  activity on that token.

    # TODO: /subscribe <token>: Tags or DM the caller when there's activity on a token by ANY target.

    # TODO: /list: Shows the list of current targets
