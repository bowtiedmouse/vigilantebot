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

    # /subscribe <alias> <token>
    @slash_command(name='subscribe', guild_ids=GUILD_IDS)
    async def subscribe_user_to_updates(
            self, ctx: discord.ApplicationContext,
            target_alias: Option(str,
                                 '(Optional) Choose a target to get updates from. Ex: Tetranode',
                                 choices=TARGETS_LIST,
                                 default=''),
            token_symbol: Option(str,
                                 '(Optional) Choose a token to get updates from. Ex: MAGIC',
                                 default='')
    ):
        """
        Will DM you with updates on the selected option (target, token or target_token combination).

        :param ctx:
        :param target_alias: Alias of target to get updates on
        :param token_symbol: A token for which activity on any target will get updates
        :param target_token: A combination of target and token, getting updates only when that
        target has updates on that token
        """
        return await sc.subscribe_user(ctx, target_alias, token_symbol)

    # /my_subscriptions
    @slash_command(name='my_subscriptions', guild_ids=GUILD_IDS)
    async def show_user_subscriptions_list(
            self, ctx: discord.ApplicationContext):
        """
        Get the list of your active subscriptions.
        """
        return await sc.show_subscriptions(ctx)

    # /unsubscribe
    @slash_command(name='unsubscribe', guild_ids=GUILD_IDS)
    async def unsubscribe_user(
            self, ctx: discord.ApplicationContext):
        """
        Will unsubscribe you to any of your subscriptions.
        """
        return await sc.unsubscribe_user(ctx)
