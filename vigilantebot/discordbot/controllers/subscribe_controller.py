# subscribe_controller.py
# Tasks for managing users' subscriptions to alerts. From commands:
#   /subscribe <target_alias> <target_address>
#   /unsubscribe
#   /my_subscriptions

from os.path import isfile
import logging

import discord

from discordbot.discord_settings import SUBSCRIPTIONS_FILE
from vigilante import fileutils
from discordbot.controllers import dm_helper as dm
from discordbot.views.confirm import confirm_action

logger = logging.getLogger(__name__)


async def subscribe_user(ctx: discord.ApplicationContext, target_alias: str, token_symbol: str):
    if not await dm.can_dm_user(ctx.interaction.user):
        await ctx.respond(
            f"Hey {ctx.interaction.user.mention}, "
            "looks like you don't allow DMs from this server.\n"
            "Please, allow DMs first and retry to `/subscribe`.",
            ephemeral=True)

    if target_alias and token_symbol:
        return await subscribe_user_to_target_token(ctx, target_alias, token_symbol.upper())

    if target_alias:
        return await subscribe_user_to_target(ctx, target_alias)

    if token_symbol:
        return await subscribe_user_to_token(ctx, token_symbol.upper())

    return await ctx.respond("I need at least a target's alias or a token symbol.", ephemeral=True)


# todo: check watched targets file
def is_a_watched_target(target_alias: str):
    return True


# todo: probably can be abstracted more
async def subscribe_user_to_target(ctx: discord.ApplicationContext, target_alias: str):
    # Autocomplete takes care of this check, so probably won't be used
    if not is_a_watched_target(target_alias):
        return await ctx.respond(
            f"Sorry, {target_alias} is not in my watch list. "
            "Use `/list` command to see what targets you can subscribe to.",
            ephemeral=True)

    confirmed = await get_subscription_confirmation(
        ctx, target_alias,
        f"Copy. I'll DM you any **{target_alias}**'s updates.")
    if not confirmed:
        return

    await add_subscription(ctx.interaction.user.id, 'targets', target_alias)


async def subscribe_user_to_token(ctx: discord.ApplicationContext, token_symbol: str):
    confirmed = await get_subscription_confirmation(
        ctx, token_symbol,
        f"Roger. I'll DM you any **{token_symbol}** updates for all watched targets.")
    if not confirmed:
        return

    await add_subscription(ctx.interaction.user.id, 'tokens', token_symbol)


async def subscribe_user_to_target_token(ctx: discord.ApplicationContext, target_alias: str,
                                         token_symbol: str):
    confirmed = await get_subscription_confirmation(
        ctx, target_alias + ' movements on ' + token_symbol,
        f"Read. I'll DM you any **{target_alias}** movements on **{token_symbol}**.")
    if not confirmed:
        return

    await add_subscription(ctx.interaction.user.id, 'target_tokens', target_alias + '_' + token_symbol)


async def get_subscription_confirmation(ctx, subscription_subject: str, confirmed_msg: str) -> bool:
    await ctx.defer()
    confirmed = await confirm_action(
        ctx,
        f"Confirm that you want to receive reports on updates for **{subscription_subject}** "
        "(will DM you).")

    if not confirmed:
        await ctx.respond('*OK, cancelling...*', ephemeral=True)
        return False

    await ctx.respond('*Confirmed!*', ephemeral=True)
    await ctx.respond(confirmed_msg, ephemeral=True)
    return True


async def show_subscriptions(ctx: discord.ApplicationContext):
    subs_list = get_user_subscriptions_list(ctx.interaction.user.id)
    return ctx.respond(f"You're receiving updates for:\n**{', '.join(subs_list)}**."
                       "\nYou can unsubscribe with the `unsubscribe` command.")


# TODO: On updates: check if token/target/target_token exists on file and DM list of users
async def add_subscription(user_id: int, subs_category: str, subs_subject: str):
    subs_data = list(
        fileutils.get_file_key_content(SUBSCRIPTIONS_FILE, subs_category, subs_subject))
    if not subs_data:
        fileutils.update_file_key(SUBSCRIPTIONS_FILE, subs_category, [], subs_subject)

    if user_id not in subs_data:
        logger.info(f'New user subscribed to {subs_category}/{subs_subject}: {user_id}.')
        subs_data.append(user_id)
        fileutils.update_file_key(SUBSCRIPTIONS_FILE, subs_category, subs_data, subs_subject)


def get_user_subscriptions_list(user_id: int) -> list:
    return ['ETH token', 'DeFiGod movements', 'Tetranode ETH movements']


def unsubscribe_user(ctx: discord.ApplicationContext):
    return None
    # remove subs_subject if empty


def create_subscriptions_file() -> None:
    fileutils.create_empty_json_file(SUBSCRIPTIONS_FILE)
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'targets')
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'tokens')
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'target_tokens')
    print(f'Created file: {SUBSCRIPTIONS_FILE}')


def subscriptions_file_exist() -> bool:
    return isfile(SUBSCRIPTIONS_FILE)
