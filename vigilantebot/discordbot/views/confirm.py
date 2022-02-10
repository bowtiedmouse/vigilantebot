import discord


class Confirm(discord.ui.View):
    """
    Define a simple View that gives us a confirmation menu
    """

    def __init__(self):
        super().__init__(timeout=120)
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # Stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="👌 Confirm", style=discord.ButtonStyle.primary)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        # await interaction.response.send_message("Confirming...", ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="👎 Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        # await interaction.response.send_message("Cancelling", ephemeral=True)
        self.value = False
        self.stop()


async def confirm_action(ctx: discord.ApplicationContext, confirmation_msg: str):
    view = Confirm()
    await ctx.send(confirmation_msg, view=view)
    await view.wait()
    return view.value
