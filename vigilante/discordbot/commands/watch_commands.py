from discord.ext import commands
from discord.commands import permissions
from discord.commands import slash_command
from discord.commands import Option
import discord

import vigilante
from discordbot.settings import GUILD_IDS, ADMIN_ROLES, TARGETS_LIST
from discordbot import processes as p


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
        return await p.watch_targets(ctx, target)

    # /stop
    @slash_command(name='stop', guild_ids=GUILD_IDS, default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    @permissions.is_owner()
    async def stop_watch(self, ctx: discord.ApplicationContext):
        """
        Stop watching activity.
        """
        return await p.stop_watching(ctx)

    # TODO: /subscribe <address or alias> <token>: Tags or DM the caller when the target has
    #  activity on that token.
    @slash_command(name='dmme', guild_ids=GUILD_IDS)
    async def send_dm(self, ctx: discord.ApplicationContext):
        return await ctx.interaction.user.send('Hello')

    @send_dm.error
    async def send_dm_error(self, ctx, error):
        # if isinstance(error, discord.commands.errors.ApplicationCommandInvokeError):
        return await ctx.respond('Error DM')

    # TODO: /subscribe <token>: Tags or DM the caller when there's activity on a token by ANY target.

    # TODO: /list: Shows the list of current targets
    @slash_command(name='list', guild_ids=GUILD_IDS)
    async def show_targets_list(self, ctx: discord.ApplicationContext):
        """
        Show the list of all watched targets.
        """
        targets_list = ', '.join(vigilante.get_targets_alias_list())
        return await ctx.respond("I'm currently watching these targets:\n"
                                 f"**{targets_list}**."
                                 "\nAdmins can add more with the `add_target` command.")
