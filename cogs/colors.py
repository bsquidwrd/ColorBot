from discord.ext import commands
import discord

class RoleColor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='change', aliases=['modify'])
    async def change(self, ctx, *, hex_color=None):
        """Update your Role Color"""
        role_name = f"USER-{ctx.author.id}"
        hexpicker = "http://hexpicker.com/"

        delete_timer = None
        if ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            delete_timer = 60

        try:
            if hex_color is None:
                await ctx.send(f"{ctx.author.mention}, please go to {hexpicker} to pick your color then run the command again with the color after the command", delete_after=delete_timer)

            else:
                # If the hex_color starts with a # remove it
                if hex_color[0] == "#":
                    hex_color = hex_color.replace('#','')

                my_role = ctx.guild.me.top_role
                my_role_position = my_role.position

                role = None
                role_position = my_role_position - 1

                # Convert hex to RGB
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

                color = discord.Color.from_rgb(rgb_color[0], rgb_color[1], rgb_color[2])
                for guild_role in ctx.guild.roles:
                    if guild_role.name == role_name:
                        role = guild_role
                        break

                if role is None:
                    role = await ctx.guild.create_role(name=role_name, reason="User did not have specific role for managing their color", permissions=discord.Permissions.none())

                await role.edit(color=color, reason=f"Updating role color to {hex_color}", position=role_position)

                if role not in ctx.author.roles:
                    await ctx.author.add_roles(role)

                await ctx.send(f"{ctx.author.mention} I have changed your role color", delete_after=delete_timer)

        except (discord.Forbidden, discord.HTTPException):
            await ctx.send(f"{ctx.author.mention} I don't have permission to edit your color role {role.mention}")

        except Exception as e:
            self.bot.log.error(type(e))
            await ctx.send("There was an error changing your role color, please contact my owner", delete_after=delete_timer)

        if delete_timer is not None:
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(RoleColor(bot))
