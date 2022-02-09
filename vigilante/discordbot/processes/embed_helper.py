from datetime import datetime

import discord

import vigilante


def format_log(alerts_log):
    updates = {}
    last_alias = ''

    for alert in alerts_log:
        if last_alias != alert.target_alias:
            updates[alert.target_alias] = {
                'alias': alert.target_alias,
                'address': vigilante.get_address_from_alias(alert.target_alias),
                'balance': '',
                'content': '',
            }
            last_alias = alert.target_alias

        if alert.action == 'usd_balance':
            updates[alert.target_alias]['balance'] = alert.log()
            continue

        updates[alert.target_alias]['content'] += '· ' + alert.log() + '\n'
    return updates


def create_embed(target_updates: dict):
    embed = discord.Embed(
        title=f"{target_updates['balance']}",
        color=discord.Color.random(seed=target_updates['address']),
        timestamp=datetime.now())

    embed.set_author(
        name=target_updates['alias'],
        url=f"https://debank.com/profile/{target_updates['address']}",
        icon_url=f'https://identicon-api.herokuapp.com/{target_updates["address"]}/100?format=png')

    embed.add_field(
        name="Last wallet movements:",
        value=target_updates['content'],
        inline=False)

    embed.set_footer(
        text="Disclaimer: balances in the target's wallet can change b/c of (un)staking, "
             "claiming, and other activities.")

    return embed
