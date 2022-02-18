# manage_controller.py
# Tasks for managing the watched targets list. Mostly admin-only. From the commands:
#   /add_target <target_alias> <target_address>
#   /remove_target <target_alias>
#   /list
import discord

from discordbot.utils.target_utils import TARGETS_LIST
from vigilante import get_addresses_from_alias
from vigilante import fileutils
from vigilante.settings import TARGET_ACCOUNTS_FILE


def is_valid_evm_address(address: str):
    if len(address) < 42:
        return False
    try:
        int(address, 16)
        return True
    except ValueError:
        return False


def get_targets_alias_list_with_addresses():
    targets_w_addresses = []
    for target_alias in TARGETS_LIST:
        addresses = get_addresses_from_alias(target_alias)
        targets_w_addresses.append(f"**{target_alias}** (*{', '.join(addresses)}*)")

    return targets_w_addresses


# todo: after add/remove the bot needs to restart
async def add_new_target(
        ctx: discord.ApplicationContext,
        target_alias: str,
        target_addresses: str
):
    await ctx.defer()
    addresses: list = target_addresses.split(' ')
    saved_targets = fileutils.get_file_dict(TARGET_ACCOUNTS_FILE)

    if (
            await check_valid_target(ctx, saved_targets, target_alias) and
            await check_valid_addresses(ctx, addresses, saved_targets)
    ):
        await save_target_to_file(ctx, addresses, target_alias)
        return True
    return False


async def save_target_to_file(ctx, addresses, target_alias):
    target_data = {
        "alias": target_alias,
        "addresses": addresses
    }
    fileutils.update_file_key(TARGET_ACCOUNTS_FILE, target_alias, target_data)

    await ctx.respond(
        f":ok_hand: Done! **{target_alias}** (*{', '.join(addresses)}*) added to my list of targets.")


async def check_valid_target(
        ctx: discord.ApplicationContext,
        saved_targets: list,
        target_alias: str
):
    if target_alias.lower() in map(str.lower, saved_targets):
        await ctx.respond(
            f'*{target_alias.title()}* is already in my targets list.',
            ephemeral=True)
        return False
    return True


async def check_valid_addresses(
        ctx: discord.ApplicationContext,
        addresses: list,
        saved_targets: dict
):
    for address in addresses:
        if not is_valid_evm_address(address):
            await ctx.respond(
                f'You gave me a wrong EVM compatible address: *{address}*',
                ephemeral=True)
            return False

        for s_alias, s_data in saved_targets.items():
            if address in s_data['addresses']:
                await ctx.respond(
                    f"I'm already watching the address *{address}* for the target *{s_alias}*.",
                    ephemeral=True)
                return False
    return True


async def remove_target(
        ctx: discord.ApplicationContext,
        target_alias: str
):
    await ctx.defer()
    saved_targets = fileutils.get_file_dict(TARGET_ACCOUNTS_FILE)

    try:
        del saved_targets[target_alias]
        fileutils.update_file(TARGET_ACCOUNTS_FILE, saved_targets)

        await ctx.respond(
            f"I've removed that sucker from my target's list (*{target_alias}*).",
            ephemeral=True)
        return True
    except KeyError:
        await ctx.respond(
            f"Looks like *{target_alias}* was already removed from my target's list.",
            ephemeral=True)
        return False
