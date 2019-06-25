from discord.ext import commands
import discord
import asyncio
import logging
import traceback
import sys
import os


description = """
Hello! I am a bot meant to alleviate the pain of assigning people Color roles!
"""

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
log.addHandler(handler)

initial_extensions = (
    'cogs.admin',
    'cogs.meta',
    'cogs.colors',
)


def _prefix_callable(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ']
    return base


class ColorBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=_prefix_callable, case_insensitive=True, description=description, pm_help=None, help_attrs=dict(hidden=True))

        self.client_token = os.environ['CLIENT_TOKEN']
        self.log = log

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                self.log.info(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()


    async def on_ready(self):
        self.log.info(f'Ready: {self.user} (ID: {self.user.id})')


    async def check(self, ctx):
        # Make sure commands are only run in a Guild
        # and not in a DM or something
        self.log.info("Check running")
        return ctx.guild is not None


    def run(self):
        super().run(self.client_token, reconnect=True)


if __name__ == '__main__':
    bot = ColorBot()
    bot.run()
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
