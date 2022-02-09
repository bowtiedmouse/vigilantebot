# watch_controller.py
# Watch tasks from the commands:
#   /watch
#   /watch <target_alias>
#   /stop

from discord.ext import tasks
import discord

from discordbot.settings import WATCH_FREQUENCY_MINUTES
from discordbot.controllers import embed_helper as emb
import vigilante

_is_watch_initial_start = True
_is_watch_restart = False


async def watch_targets(ctx: discord.ApplicationContext, target_alias: str = ''):
    """
    Start a watch turn on all targets or one target if it's specified.
    """
    global _is_watch_restart
    await ctx.defer()

    if target_alias:
        return await watch_one_target(ctx, target_alias)

    if watch_all_targets_task.is_running():
        await ctx.respond("Ooooo I'm watchiiiiiing...")
        _is_watch_restart = True
        return watch_all_targets_task.restart(ctx)

    await ctx.respond(ctx.interaction.user.mention +
                      " asked me to start my watch turn on all targets.\nI'm a watchoooooooor!")
    return await watch_all_targets_task.start(ctx)


@tasks.loop(minutes=WATCH_FREQUENCY_MINUTES)
async def watch_all_targets_task(ctx: discord.ApplicationContext):
    """
    Main watch task. Will watch all targets in the list and report embeds when there are updates.
    """
    global _is_watch_initial_start
    global _is_watch_restart

    updates = vigilante.watch_targets()
    if updates:
        return await report_updates(ctx, updates,
                                    mention_user=_is_watch_initial_start or _is_watch_restart)

    if _is_watch_initial_start:
        _is_watch_initial_start = False
        return await ctx.respond("No updates yet! I'll report updates regularly to this channel.")

    if _is_watch_restart:
        _is_watch_restart = False
        return await ctx.respond("No updates yet!")


async def watch_one_target(ctx: discord.ApplicationContext, target_alias: str):
    """
    Will watch only one target and report any updates. This is NOT a task, so it'll be executed
    only once, by command request.
    """
    await ctx.respond(f'Wait a sec while I watch {target_alias}...')

    updates = vigilante.watch_target(target_alias)
    if updates:
        return await report_updates(ctx, updates, target_alias)

    return await ctx.respond(f"{target_alias}'s clean. Nothing to report yet.")


async def report_updates(ctx, alerts_log: list, target_alias: str = '', mention_user: bool = False):
    """
    Send any updates to the channel.
    """
    response_msg = f"Hey {ctx.interaction.user.mention}, " if mention_user else ''
    await ctx.send(response_msg + "I have some updates. I'm reportiiiiing!")

    updates = emb.format_log(alerts_log)

    if target_alias:
        return await ctx.send(embed=emb.create_embed(updates[target_alias]))

    embeds = [emb.create_embed(target_updates) for target_updates in updates.values()]
    return await ctx.send(embeds=embeds)


async def stop_watching(ctx: discord.ApplicationContext):
    """
    Stop the active watching task.
    """
    await ctx.respond('Oki!')
    watch_all_targets_task.stop()
    return await ctx.send("I've stopped watching. Will grab a bear and relax for a bit.")
