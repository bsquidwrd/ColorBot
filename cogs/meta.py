from discord.ext import commands
import asyncio
import discord

class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True)
    async def hello(self, ctx):
        """Displays my intro message."""
        app_info = await self.bot.application_info()
        await ctx.send('Hello! I\'m a robot! {0.name}#{0.discriminator} made me.'.format(app_info.owner))
        
    
    @commands.command(name='invite')
    async def invite(self, ctx):
        """Send invite link"""
        app_info = await self.bot.application_info()
        if app_info.bot_public:
            await ctx.send(f"Here is my invite link: <https://discordapp.com/oauth2/authorize?client_id={app_info.id}&scope=bot&permissions=268445696>")


def setup(bot):
    bot.add_cog(Meta(bot))
