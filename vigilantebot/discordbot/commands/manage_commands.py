from discord.ext import commands
from discord.commands import permissions
from discord.commands import slash_command
from discord.commands import Option
import discord

from discordbot.discord_settings import ADMIN_ROLES, TARGETS_LIST
from discordbot.controllers import manage_controller as mc


class ManageTargetsCommands(commands.Cog):
    """
    Commands only for admins: to add, edit or remove targets.
    """

    def __init__(self, _bot):
        self.bot = _bot

    # /add_target <address> <alias>
    @slash_command(name='add_target', default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    @permissions.is_owner()
    async def add_target_command(
            self, ctx: discord.ApplicationContext,
            alias: Option(
                str,
                'Give this target an alias. Ex: Tetranode'),
            *,
            address: Option(
                str,
                'The addresses for this target (separated by spaces). Ex: 0x9abc123...')
    ):
        """
        Adds a new target to watch.
        """
        return await mc.add_new_target(ctx, alias, address)

    # /remove_target
    @slash_command(name='remove_target', default_permission=False)
    @permissions.has_any_role(*ADMIN_ROLES)
    @permissions.is_owner()
    async def remove_target_command(
            self, ctx: discord.ApplicationContext,
            target_alias: Option(str,
                                 '(Optional) Choose a target to remove from the list.',
                                 choices=TARGETS_LIST,
                                 default='')
    ):
        """
        Remove a target from the watch list.
        """
        return await mc.remove_target(ctx, target_alias)

    # /list
    @slash_command(name='list')
    async def show_targets_list(self, ctx: discord.ApplicationContext):
        """
        Show the list of all watched targets.
        """
        targets_list = '\n\n'.join(mc.get_targets_alias_list_with_addresses())
        return await ctx.respond("I'm currently watching these targets:\n\n"
                                 f"{targets_list}."
                                 "\n\nAdmins can add more with the `add_target` command.")

    # async def reset_cog(self):
    #     await bot_utils.reset_bot_cogs(self.bot, self)
