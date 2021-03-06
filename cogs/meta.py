from discord.ext import commands
import asyncio
import discord


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)


    def add_bot_commands_formatting(self, commands, heading):
        if commands:
            joined = ', '.join(c.name for c in commands)
            self.paginator.add_line('__**%s**__' % heading)
            self.paginator.add_line(joined)


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self


    def cog_unload(self):
        self.bot.help_command = self.old_help_command


    @commands.command(hidden=True)
    async def hello(self, ctx):
        """Displays my intro message."""
        app_info = await self.bot.application_info()
        await ctx.send('Hello! I\'m a robot! {0.name}#{0.discriminator} made me.'.format(app_info.owner))


    @commands.command(name='invite')
    async def invite(self, ctx):
        """Send invite link"""
        app_info = await self.bot.application_info()
        if app_info.bot_public or ctx.author == app_info.owner:
            await ctx.send(f"{ctx.author.mention}, here is my invite link: <https://discordapp.com/oauth2/authorize?client_id={app_info.id}&scope=bot&permissions=268445696>")
        else:
            await ctx.send(f"{ctx.author.mention}, it looks like I'm not available publicly yet")


def setup(bot):
    bot.add_cog(Meta(bot))
