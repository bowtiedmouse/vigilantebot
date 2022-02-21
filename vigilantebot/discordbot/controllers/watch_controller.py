# watch_controller.py
# Watch tasks from the commands:
#   /watch
#   /watch <target_alias>
#   /stop
import asyncio
import logging

from discord.ext import tasks
import discord

from discordbot.discord_settings import WATCH_FREQUENCY_SECONDS
from discordbot.utils import embed_utils as emb
from discordbot.controllers import subscribe_controller as sc
import vigilante

logger = logging.getLogger(__name__)

# Will switch off only once unless watch task is stopped
_is_watch_initial_start = True
# For anytime that a /watch command is used and task was already running
_is_watch_restart = False
# vigilante.watch_targets() is still running, so better let it finish or won't get updates ever
_is_watch_updating = False
# When using /watch <target_alias> is better to let one target finish before start a new one
# todo: maybe it's better to not launch any watch task at once
_target_currently_watching = [str]


async def watch_targets(
        ctx: discord.ApplicationContext,
        target_alias: str = ''):
    """
    Start a watch turn on all targets or one target if it's specified.
    """
    global _is_watch_restart
    global _is_watch_updating
    await ctx.defer()

    if _is_watch_updating:
        return await ctx.respond("I'm on it! If there are updates I'll report soon™.")

    if target_alias:
        return await watch_one_target(ctx, target_alias)

    if watch_all_targets_task.is_running():
        await ctx.respond("Ooooo I'm watchiiiiiing...")

        _is_watch_restart = True
        return watch_all_targets_task.restart(ctx)

    await ctx.respond(ctx.interaction.user.mention +
                      " asked me to start my watch turn on all targets.\nI'm a watchoooooooor!")
    return await watch_all_targets_task.start(ctx)


@tasks.loop(seconds=WATCH_FREQUENCY_SECONDS)
async def watch_all_targets_task(ctx: discord.ApplicationContext):
    """
    Main watch task. Will watch all targets in the list and report embeds when there are updates.
    """
    global _is_watch_initial_start
    global _is_watch_restart
    global _is_watch_updating

    # Avoid processing multiple watch tasks at once
    _is_watch_updating = True
    updates = vigilante.watch_targets()
    _is_watch_updating = False

    if updates:
        if updates[0] == 'no_targets':
            return await ctx.respond("I'm not watching any targets. Admins have to add them first with `add_target`.")
        return await report_updates(
            ctx, updates,
            mention_user=_is_watch_initial_start or _is_watch_restart)

    if _is_watch_initial_start:
        _is_watch_initial_start = False
        return await ctx.respond("No updates yet! I'll report updates regularly to this channel.")

    if _is_watch_restart:
        _is_watch_restart = False
        return await ctx.respond("No updates yet!")


async def watch_one_target(
        ctx: discord.ApplicationContext,
        target_alias: str):
    """
    Will watch only one target and report any updates. This is NOT a task, so it'll be executed
    only once, by command request.
    """
    global _is_watch_updating
    await ctx.respond(f'Wait a sec while I watch {target_alias}...')

    # Avoid watching target if a watch tasks is already running
    while _is_watch_updating:
        await asyncio.sleep(5)

    updates = vigilante.watch_target(target_alias)

    if updates:
        return await report_updates(ctx, updates, target_alias)

    return await ctx.respond(f"{target_alias}'s clean. Nothing to report yet.")


async def report_updates(
        ctx: discord.ApplicationContext,
        updates: list,
        target_alias: str = '',
        mention_user: bool = False):
    """
    Send any updates to the channel.
    """
    alerts_log = emb.format_log(updates)
    await sc.report_updates_to_subscribers(ctx, alerts_log)

    response_msg = f"Hey {ctx.interaction.user.mention}, " if mention_user else ''
    await ctx.send(response_msg + "I have some updates. I'm reportiiiiing!")

    if target_alias:
        return await ctx.send(embed=emb.create_update_report_embed(alerts_log[target_alias]))

    embeds = [
        emb.create_update_report_embed(target_updates)
        for target_updates in alerts_log.values()
        if target_updates['content']
    ]

    if embeds:
        return await ctx.send(embeds=embeds)


async def stop_watching(ctx: discord.ApplicationContext):
    """
    Stop the active watching task.
    """
    global _is_watch_initial_start
    _is_watch_initial_start = True

    watch_all_targets_task.stop()
    logging.info('Watching stopped by user.')
    return await ctx.send("I've stopped watching. Will grab a bear and relax for a bit.")
