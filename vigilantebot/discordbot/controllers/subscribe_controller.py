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
from discordbot.utils import dm_utils as dm
from discordbot.views.confirm import confirm_action
from discordbot.views.dropdown import select_multiple_options
from discordbot.utils import embed_utils as emb

logger = logging.getLogger(__name__)


async def subscribe_user(
        ctx: discord.ApplicationContext,
        target_alias: str,
        token_symbol: str
):
    if not await dm.can_dm_user(ctx.interaction.user):
        await ctx.respond(
            f"Hey {ctx.interaction.user.mention}, "
            "looks like you don't allow DMs from this server.\n"
            "Please, allow DMs first and retry to `/subscribe`.",
            ephemeral=True,
            file=discord.File(fp="discordbot/resources/shall-not-pass.gif",
                              filename="shall-not-pass.gif")
        )

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


async def subscribe_user_to_target_token(
        ctx: discord.ApplicationContext,
        target_alias: str,
        token_symbol: str
):
    confirmed = await get_subscription_confirmation(
        ctx, target_alias + ' movements on ' + token_symbol,
        f"Read. I'll DM you any **{target_alias}** movements on **{token_symbol}**.")
    if not confirmed:
        return

    await add_subscription(ctx.interaction.user.id, 'target_tokens',
                           target_alias + '_' + token_symbol)


async def get_subscription_confirmation(
        ctx: discord.ApplicationContext,
        subscription_subject: str,
        confirmed_msg: str
) -> bool:
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
    subs_list = [sub['description'] for sub in get_user_subscriptions_list(ctx.interaction.user.id)]
    return await ctx.respond(f"You're receiving updates for:\n**{', '.join(subs_list)}**."
                             "\nYou can cancel any subscription with the `unsubscribe` command.")


async def add_subscription(
        user_id: int,
        subs_category: str,
        subs_subject: str
):
    subs_data = list(
        fileutils.get_file_key_content(SUBSCRIPTIONS_FILE, subs_category, subs_subject))
    if not subs_data:
        fileutils.update_file_key(SUBSCRIPTIONS_FILE, subs_category, [], subs_subject)

    if user_id not in subs_data:
        logger.info(f'New user subscribed to {subs_category}/{subs_subject}: {user_id}.')
        subs_data.append(user_id)
        fileutils.update_file_key(SUBSCRIPTIONS_FILE, subs_category, subs_data, subs_subject)


def get_user_subscriptions_list(user_id: int) -> list:
    user_subscriptions = []
    subs_data = fileutils.get_file_dict(SUBSCRIPTIONS_FILE)

    for category in subs_data.keys():
        suffix = ' token' if category == 'tokens' else ' movements'

        for key, subscribers in subs_data[category].items():
            desc = key.replace('_', '\'s ') + suffix
            if user_id in subscribers:
                user_subscriptions.append({'label': key, 'description': desc})

    return user_subscriptions


async def unsubscribe_user(ctx: discord.ApplicationContext):
    user_subs = get_user_subscriptions_list(ctx.interaction.user.id)
    if not user_subs:
        ctx.respond("You don't have any active subscription yet. Add one with `/subscribe` command.")

    await ctx.defer()
    # Show the dropdown and wait for user's choice
    return await select_multiple_options(
        ctx,
        select_options=user_subs,
        message="Which subscription(s) do you want to cancel?",
        callback_fn=unsubscribe_user_from_selected_options
    )


# This is the callback from the dropdown component
async def unsubscribe_user_from_selected_options(
        interaction: discord.Interaction,
        values: list
):
    await interaction.response.send_message(f"hey : {', '.join(values)}", ephemeral=True)
    # remove subs_subject if empty
    # todo: actually unsubscribe users


# def get_active_subscriptions() -> list:
#     subs_data = fileutils.get_file_dict(SUBSCRIPTIONS_FILE)
#     return [subject for content in subs_data.values() for subject in list(content.keys())]


# TODO: an improved version should send the same update only once (ex. if user is subscribed to
#  a target, a token, and for that target-token combination, will receive the same updates 3 times.
#  Or even if he is subscribed to a target and a token, and that target had movement on that token,
#  he will receive the same message twice.
async def report_updates_to_subscribers(
        ctx: discord.ApplicationContext,
        updates: dict
) -> None:
    subscriptions = fileutils.get_file_dict(SUBSCRIPTIONS_FILE)

    await report_target_updates_to_subscribers(ctx, subscriptions, updates)
    await report_token_updates_to_subscribers(ctx, subscriptions, updates)
    await report_target_token_updates_to_subscribers(ctx, subscriptions, updates)


async def report_target_token_updates_to_subscribers(
        ctx: discord.ApplicationContext,
        subscriptions: dict,
        updates: dict
):
    for target_token in subscriptions['target_tokens'].keys():
        sub_target, sub_token = target_token.split('_')
        for up_target_data in updates.values():
            if sub_target == up_target_data['alias'] and sub_token in up_target_data['content']:
                await send_update_to_subscriber(
                    user=ctx.interaction.user,
                    updated_key=target_token,
                    target_updates_data=up_target_data
                )


async def report_token_updates_to_subscribers(
        ctx: discord.ApplicationContext,
        subscriptions: dict,
        updates: dict
):
    for token in subscriptions['tokens'].keys():
        for target_data in updates.values():
            if token in target_data['content']:
                # The name of the token is in the long message in `content`
                await send_update_to_subscriber(
                    user=ctx.interaction.user,
                    updated_key=token,
                    target_updates_data=updates[target_data['alias']]
                )


async def report_target_updates_to_subscribers(
        ctx: discord.ApplicationContext,
        subscriptions: dict,
        updates: dict
):
    for target in subscriptions['targets'].keys():
        if target in updates:
            await send_update_to_subscriber(
                user=ctx.interaction.user,
                updated_key=target,
                target_updates_data=updates[target]
            )


async def send_update_to_subscriber(
        user: discord.User,
        updated_key: str,
        target_updates_data: dict
):
    try:
        return await user.send(
            f"Hey {user.display_name}! I have some news on **{updated_key}** for you:",
            embed=emb.create_update_report_embed(target_updates_data))
    except KeyError as e:
        logger.error('KeyError %s when sending %s updates with data %s',
                     e, updated_key, target_updates_data)


def create_subscriptions_file() -> None:
    fileutils.create_empty_json_file(SUBSCRIPTIONS_FILE)
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'targets')
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'tokens')
    fileutils.create_empty_key_in_file(SUBSCRIPTIONS_FILE, 'target_tokens')
    print(f'Created file: {SUBSCRIPTIONS_FILE}')


def subscriptions_file_exist() -> bool:
    return isfile(SUBSCRIPTIONS_FILE)
