from typing import Callable, Coroutine

import discord


class SelectMultiple(discord.ui.Select):
    def __init__(
            self, options: list[discord.SelectOption],
            callback_fn: Callable[[discord.Interaction, list], Coroutine]
    ):
        super().__init__(
            placeholder="You can choose multiple options",
            min_values=1,
            max_values=len(options),
            options=options,
        )
        self.callback_fn = callback_fn

    # Select component will call this after any user's change of choices (even after the first one)
    async def callback(self, interaction: discord.Interaction):
        await self.callback_fn(interaction, self.values)


class DropdownView(discord.ui.View):
    def __init__(
            self, options: list[discord.SelectOption],
            callback_fn: Callable[[discord.Interaction, list], Coroutine]
    ):
        super().__init__()
        self.add_item(SelectMultiple(options, callback_fn))

    def clear(self):
        self.children.clear()


async def select_multiple_options(
        ctx: discord.ApplicationContext,
        select_options: list,
        message: str,
        callback_fn: Callable[[discord.Interaction, list], Coroutine]
) -> [str]:
    """
    Send a message with a dropdown containing a list of choices and return selected values.
    """
    view = DropdownView(get_select_options(select_options), callback_fn)
    await ctx.respond(message, view=view, ephemeral=True)
    # await view.wait()
    return view.children[0].values


def get_select_options(options: list):
    return [
        discord.SelectOption(
            label=option['label'], description=option['description'], emoji="👁‍🗨"
        )
        for option in options]
