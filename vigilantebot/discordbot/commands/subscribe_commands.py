from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option
import discord

from discordbot.discord_settings import GUILD_IDS, TARGETS_LIST
from discordbot.controllers import subscribe_controller as sc


class SubscribeCommands(commands.Cog):
    """
    Commands for subscribe users to tokens/targets alerts and DM them with updates.
    """

    def __init__(self, _bot):
        self.bot = _bot

    # TODO: /subscribe <alias> <token>: Tags or DM the caller when there is activity on
    #  a target, a token, or a target-token combination
    @slash_command(name='subscribe', guild_ids=GUILD_IDS)
    async def subscribe_user_to_updates(
            self, ctx: discord.ApplicationContext,
            target_alias: Option(str,
                                 '(Optional) Choose a target to get updates from. Ex: Tetranode',
                                 choices=TARGETS_LIST, default=''),
            token_symbol: Option(str, '(Optional) Choose a token to get updates from. Ex: MAGIC',
                                 default='')
    ):
        """
        DMs the caller with updates on the selected option (target, token or target_token combination).

        :param ctx:
        :param target_alias: Alias of target to get updates on
        :param token_symbol: A token for which activity on any target will get updates
        :param target_token: A combination of target and token, getting updates only when that
        target has updates on that token
        """
        return await sc.subscribe_user(ctx, target_alias, token_symbol)

    @subscribe_user_to_updates.error
    async def send_dm_error(self, ctx, error):
        # if isinstance(error, discord.commands.errors.ApplicationCommandInvokeError):
        return await ctx.respond('Error DM')

    # TODO: /unsubscribe: Removes user for some of the subscriptions. Will show Dropdown.
    @slash_command(name='unsubscribe', guild_ids=GUILD_IDS)
    async def unsubscribe_user(
            self, ctx: discord.ApplicationContext):
        """
        Unsubscribes the caller to any of his subscriptions or all at once.
        """
        return await sc.unsubscribe_user(ctx)

    # TODO: /my_subscriptions: Get user's subscriptions
    @slash_command(name='my_subscriptions', guild_ids=GUILD_IDS)
    async def unsubscribe_user(
            self, ctx: discord.ApplicationContext):
        """
        Get the list of active subscriptions.
        """
        return await sc.show_subscriptions(ctx)
