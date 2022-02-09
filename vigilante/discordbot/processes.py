from datetime import datetime

from discord.ext import tasks
import discord

from discordbot.settings import WATCH_FREQUENCY_MINUTES
import vigilante


async def watch_targets(ctx: discord.ApplicationContext, target_alias: str):
    """
    Start a watch turn on all targets or one target if it's specified.
    """
    await ctx.defer()
    if target_alias:
        with ctx.typing():
            await ctx.respond(f'Wait a sec while I watch {target_alias}...')
            return await watch_one_target(ctx, target_alias)

    if watch_all_targets_task.is_running():
        await ctx.respond("Oooh I'm watchiiiing. Give me a sec...")
        return watch_all_targets_task.restart(ctx)

    await ctx.respond(ctx.interaction.user.mention +
                      " asked me to start my watch turn on all targets.\nI'm a watchoooooooor!")
    return await watch_all_targets_task.start(ctx)


@tasks.loop(minutes=WATCH_FREQUENCY_MINUTES)
async def watch_all_targets_task(ctx: discord.ApplicationContext):
    return await watch_all_targets(ctx)


async def watch_all_targets(ctx):
    with ctx.typing():
        updates = vigilante.watch_targets()
        if updates:
            return await send_embeds_from_updates(ctx, updates)
        return await ctx.respond("No updates yet! I'll report updates regularly to this channel.")


async def watch_one_target(ctx: discord.ApplicationContext, target_alias: str):
    updates = vigilante.watch_target(target_alias)
    if updates:
        return await send_embeds_from_updates(ctx, updates, target_alias)
    return await ctx.respond(f"{target_alias}'s clean. Nothing to report yet.")


async def send_embeds_from_updates(ctx, alerts_log: list, target_alias: str = ''):
    await ctx.send(f"Hey {ctx.interaction.user.mention}, I have some updates. I'm reportiiiing!")
    updates = format_log(alerts_log)

    if target_alias:
        return await ctx.send(embed=create_embed(updates[target_alias]))

    for target_updates in updates.values():
        return await ctx.send(embed=create_embed(target_updates))


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
    embed.set_author(name=target_updates['alias'],
                     url=f"https://debank.com/profile/{target_updates['address']}",
                     icon_url=f'https://identicon-api.herokuapp.com/{target_updates["address"]}/100?format=png')

    embed.add_field(name="Last wallet movements:", value=target_updates['content'],
                    inline=False)

    embed.set_footer(
        text="Disclaimer: balances in the target's wallet can change b/c of (un)staking, "
             "claiming, and other activities.")

    return embed


async def stop_watching(ctx: discord.ApplicationContext):
    await ctx.respond('Oki!')
    watch_all_targets_task.stop()
    return await ctx.send("I've stopped watching. Will grab a bear and relax for a bit.")