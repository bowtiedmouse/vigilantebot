# subscribe_controller.py
# Tasks for managing users' subscriptions to alerts. From commands:
#   /subscribe <target_alias> <target_address>
#   /unsubscribe
#   /my_subscriptions

from os.path import isfile

import discord

from discordbot.discord_settings import SUBSCRIPTIONS_FILE
from vigilante import fileutils


async def subscribe_user(ctx: discord.ApplicationContext, target_alias: str, token_symbol: str):
    if target_alias and token_symbol:
        return await subscribe_user_to_target_token(ctx, target_alias, token_symbol)

    if target_alias:
        return await subscribe_user_to_target(ctx, target_alias)

    if token_symbol:
        return await subscribe_user_to_token(ctx, token_symbol)

    return await ctx.respond('I need at least a target alias or a token symbol.', ephemeral=True)


async def subscribe_user_to_target(ctx: discord.ApplicationContext, target_alias: str):
    return await ctx.respond(
        f"Copy that! I'll DM you any **{target_alias}**'s updates.", ephemeral=True)


async def subscribe_user_to_token(ctx: discord.ApplicationContext, token_symbol: str):
    return await ctx.respond(
        f"Copy that! I'll DM you any **{token_symbol}** updates for all watched targets.",
        ephemeral=True)


async def subscribe_user_to_target_token(ctx: discord.ApplicationContext, target_alias: str,
                                         token_symbol: str):
    return await ctx.respond(
        f"Copy that! I'll DM you any **{target_alias}**'s movements on **{token_symbol}**.", ephemeral=True)


def show_subscriptions(ctx: discord.ApplicationContext):
    subs_list = get_user_subscriptions_list(ctx.interaction.user.id)
    return ctx.respond(f"You're receiving updates for:\n**{', '.join(subs_list)}**."
                       "\nYou can unsubscribe for any of them with the `unsubscribe` command.")


def get_user_subscriptions_list(user_id: int) -> list:
    return ['ETH token', 'DeFiGod movements', 'Tetranode ETH movements']


def unsubscribe_user(ctx: discord.ApplicationContext):
    return None


def create_subscriptions_file() -> None:
    fileutils.create_empty_json_file(SUBSCRIPTIONS_FILE)
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'targets')
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'tokens')
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'target_tokens')
    print(f'Created file: {SUBSCRIPTIONS_FILE}')


def subscriptions_file_exist() -> bool:
    return isfile(SUBSCRIPTIONS_FILE)
