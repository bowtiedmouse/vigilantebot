from discord.ext import commands
from discord.commands import permissions
from discord.commands import slash_command
from discord.commands import Option
import discord

from discordbot.discord_settings import ADMIN_ROLES, TARGETS_LIST
from discordbot.controllers import watch_controller as wc


class WatchCommands(commands.Cog):
    """
    Commands for set alerts and get updates on targets.
    """

    def __init__(self, _bot):
        self.bot = _bot

    # /watch [target_alias]
    @slash_command(name='watch')
    async def watch(self, ctx: discord.ApplicationContext,
                    target: Option(str, '(Optional) Choose a target',
                                   choices=TARGETS_LIST, default='')
                    ):
        """
        Start a watch turn on all targets or on the selected target. Options: `target <alias>`.

        If no target selected, will report regularly.
        """
        return await wc.watch_targets(ctx, target)

    # /stop
    @slash_command(name='stop', default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    @permissions.is_owner()
    async def stop_watch(self, ctx: discord.ApplicationContext):
        """
        Stop recurrent watching task.
        """
        return await wc.stop_watching(ctx)
