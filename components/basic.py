import random

import twitchio
from twitchio.ext import commands


class BasisComponent(commands.Component):
    # An example of a Component with some simple commands and listeners
    # You can use Components within modules for a more organized codebase and hot-reloading.

    def __init__(self, *args, bot: commands.AutoBot, **kwargs) -> None:
        self.bot = bot
        self.owner = bot.create_partialuser(user_id=bot.owner_id)

    # An example of listening to an event
    # We use a listener in our Component to display the messages received.
    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")
        # this thing is recursive as is
        # await self.owner.send_message(
        #     sender=self.bot.user,
        #     message=f"Message from {payload.chatter.name}: {payload.text}",
        # )

    # @commands.command()
    # async def test(self, ctx: commands.Context, id: str) -> None:
    #     await ctx.chatter.send_shoutout(to_broadcaster=id, moderator=id)
    #     await ctx.send(
    #         f"There should be a shoutout for {ctx.chatter}, if no smth went wrong."
    #     )

    @commands.command()
    async def hi(self, ctx: commands.Context) -> None:
        """Command that replies to the invoker with Hi <name>!

        !hi
        """
        await ctx.reply(f"Hi {ctx.chatter}!")

    @commands.command()
    async def say(self, ctx: commands.Context, *, message: str) -> None:
        """Command which repeats what the invoker sends.

        !say <message>
        """
        await ctx.send(message)

    @commands.command()
    async def add(self, ctx: commands.Context, left: int, right: int) -> None:
        """Command which adds to integers together.

        !add <number> <number>
        """
        await ctx.reply(f"{left} + {right} = {left + right}")

    @commands.command()
    async def choice(self, ctx: commands.Context, *choices: str) -> None:
        """Command which takes in an arbitrary amount of choices and randomly chooses one.

        !choice <choice_1> <choice_2> <choice_3> ...
        """
        await ctx.reply(
            f"You provided {len(choices)} choices, I choose: {random.choice(choices)}"
        )

    @commands.command(aliases=["thanks", "thank"])
    async def give(
        self,
        ctx: commands.Context,
        user: twitchio.User,
        amount: int,
        *,
        message: str | None = None,
    ) -> None:
        """A more advanced example of a command which has makes use of the powerful argument parsing, argument converters and
        aliases.

        The first argument will be attempted to be converted to a User.
        The second argument will be converted to an integer if possible.
        The third argument is optional and will consume the reast of the message.

        !give <@user|user_name> <number> [message]
        !thank <@user|user_name> <number> [message]
        !thanks <@user|user_name> <number> [message]
        """
        msg = f"with message: {message}" if message else ""
        await ctx.send(
            f"{ctx.chatter.mention} gave {amount} thanks to {user.mention} {msg}"
        )

    @commands.group(invoke_fallback=True)
    async def socials(self, ctx: commands.Context) -> None:
        """Group command for our social links.

        !socials
        """
        await ctx.send("discord.gg/..., youtube.com/..., twitch.tv/...")

    @socials.command(name="discord")
    async def socials_discord(self, ctx: commands.Context) -> None:
        """Sub command of socials that sends only our discord invite.

        !socials discord
        """
        await ctx.send("discord.gg/...")
