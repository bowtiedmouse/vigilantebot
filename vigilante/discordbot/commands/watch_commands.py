from discord.ext import commands
from discord.commands import permissions
from discord.commands import slash_command
from discord.commands import Option
import discord

from discordbot.settings import GUILD_IDS, ADMIN_ROLES, TARGETS_LIST
from ..processes import watch_processes as wp


class WatchCommands(commands.Cog):
    """
    Commands for set alerts and get updates on targets.
    """

    def __init__(self, _bot):
        self.bot = _bot

    # /watch [target_alias]
    @slash_command(name='watch', guild_ids=GUILD_IDS)
    async def watch(self, ctx: discord.ApplicationContext,
                    target: Option(str, '(Optional) Choose a target',
                                   choices=TARGETS_LIST, default='')
                    ):
        """
        Start a watch turn on all targets or on the selected target. Options: `target <alias>`.

        If no target selected, will report regularly.
        """
        return await wp.watch_targets(ctx, target)

    # /stop
    @slash_command(name='stop', guild_ids=GUILD_IDS, default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    @permissions.is_owner()
    async def stop_watch(self, ctx: discord.ApplicationContext):
        """
        Stop watching activity.
        """
        return await wp.stop_watching(ctx)
