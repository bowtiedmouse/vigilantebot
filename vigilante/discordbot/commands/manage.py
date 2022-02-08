from discord.ext import commands
from discord.commands import permissions
from discord.commands import slash_command
import discord

from discordbot.settings import GUILD_IDS, ADMIN_ROLES


class ManageTargetsCommands(commands.Cog):
    """
    Commands only for admins: to add, edit or remove targets.
    """

    def __init__(self, _bot):
        self.bot = _bot

    # TODO: /add_target <address> <alias> [avatar]: @only_admin Adds a new target to the watch list.
    @slash_command(name='add_target', guild_ids=GUILD_IDS, default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    @permissions.is_owner()
    async def add_target_command(self, ctx: discord.ApplicationContext):
        await ctx.respond("Add target command!")

    # TODO: /remove_target <alias>: @only_admin Removes a target from the watch list.
    @slash_command(name='remove_target', guild_ids=GUILD_IDS, default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    @permissions.is_owner()
    async def remove_target_command(self, ctx: discord.ApplicationContext):
        await ctx.respond("Remove target command!")
