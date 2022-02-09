from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option
import discord

from discordbot.settings import GUILD_IDS, TARGETS_LIST
from ..processes import subscribe_processes as sp


class SubscribeCommands(commands.Cog):
    """
    Commands for subscribe users to tokens/targets alerts and DM them with updates.
    """

    def __init__(self, _bot):
        self.bot = _bot

    # TODO: /subscribe <address or alias> <token>: Tags or DM the caller when the target has
    #  activity on that token.
    @slash_command(name='dmme', guild_ids=GUILD_IDS)
    async def send_dm(self, ctx: discord.ApplicationContext,
                    target: Option(str, '(Optional) Choose a target',
                                   choices=TARGETS_LIST, default='')
                    ):
        return await ctx.interaction.user.send('Hello')

    @send_dm.error
    async def send_dm_error(self, ctx, error):
        # if isinstance(error, discord.commands.errors.ApplicationCommandInvokeError):
        return await ctx.respond('Error DM')

    # TODO: /subscribe <token>: Tags or DM the caller when there's activity on a token by ANY target.

    # TODO: /subscribe <alias>: Tags or DM the caller when there's activity on a target.
