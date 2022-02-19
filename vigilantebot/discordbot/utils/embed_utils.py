from datetime import datetime
import logging

import discord

import vigilante

logger = logging.getLogger(__name__)


def format_log(alerts_log) -> dict:
    """
    Format a list of SortableAlert items into a plain dict.
    :param alerts_log: [SortableAlert]

    End format:
    updates = {
        'Whale 1': {
            'alias': 'Whale 1',
            'address': '0xa9999...',
            'balance': 'Total USD balance: $660,005',
            'content': '· Token removed: **WETH** (on *eth*). Previous balance: 2.598634407...'},
        'Whale 2': {
            'alias': 'Whale 2',
            'address': '0xe1111',
            'balance': 'Total USD balance: $616,802',
            'content': '· New token: **CVXFXS** (on *eth*). Balance: 1558.8046700736468 (5.4% ...'}
    }
    """
    updates = {}
    last_alias = ''

    for alert in alerts_log:
        if last_alias != alert.target_alias:
            updates[alert.target_alias] = {
                'alias': alert.target_alias,
                'address': vigilante.get_addresses_from_alias(alert.target_alias)[0],
                'balance': '',
                'content': '',
            }
            last_alias = alert.target_alias

        if alert.action == 'usd_balance':
            updates[alert.target_alias]['balance'] = alert.log()
            continue

        updates[alert.target_alias]['content'] += '· ' + alert.log() + '\n'

    return updates


def create_update_report_embed(target_updates: dict) -> discord.Embed:
    """
    Creates an Embed with the data of the updates on one target.
    :param target_updates: dict with the content of that target's updates.
    """
    logger.debug(f"Creating updates Embed with data: {target_updates}")
    if not target_updates['content']:
        logger.error(f"Content of the update was empty for {target_updates['alias']}")

    embed = discord.Embed(
        title=f"{target_updates['balance']}",
        color=discord.Color.random(seed=target_updates['address']),
        timestamp=datetime.now())

    embed.set_author(
        name=target_updates['alias'],
        url=f"https://debank.com/profile/{target_updates['address']}",
        icon_url=f'https://identicon-api.herokuapp.com/{target_updates["address"]}/100?format=png')
    # If identicon-api shuts down, alternative is utils.blockies.get_blockie()

    embed.add_field(
        name="Last wallet movements:",
        value=target_updates['content'],
        inline=False)

    embed.set_footer(
        text="Data from DeBank. Balances in target's wallet can change b/c of (un)staking, "
             "claiming, and other activities.")

    return embed
