from discord.ext import commands
from discord.commands import permissions
from discord.commands import slash_command
import discord

from discordbot.settings import GUILD_IDS, ADMIN_ROLES
from ..controllers import manage_controller as mc


class ManageTargetsCommands(commands.Cog):
    """
    Commands only for admins: to add, edit or remove targets.
    """

    def __init__(self, _bot):
        self.bot = _bot

    # todo: uncomment is_owner after testing permissions
    # TODO: /add_target <address> <alias> [avatar]: @only_admin Adds a new target to the watch list.
    @slash_command(name='add_target', guild_ids=GUILD_IDS, default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    # @permissions.is_owner()
    async def add_target_command(self, ctx: discord.ApplicationContext):
        await ctx.respond("Add target command!")
        raise commands.CheckFailure

    # @add_target_command.error
    # async def add_target_error(self, ctx, error):
    #     return await ctx.respond(
    #         error, ephemeral=True
    #     )  # ephemeral makes "Only you can see this" message

    # TODO: /remove_target <alias>: @only_admin Removes a target from the watch list.
    @slash_command(name='remove_target', guild_ids=GUILD_IDS, default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    @permissions.is_owner()
    async def remove_target_command(self, ctx: discord.ApplicationContext):
        await ctx.respond("Remove target command!")

    # /list
    @slash_command(name='list', guild_ids=GUILD_IDS)
    async def show_targets_list(self, ctx: discord.ApplicationContext):
        """
        Show the list of all watched targets.
        """
        targets_list = ', '.join(mc.get_targets_alias_list())
        return await ctx.respond("I'm currently watching these targets:\n"
                                 f"**{targets_list}**."
                                 "\nAdmins can add more with the `add_target` command.")
