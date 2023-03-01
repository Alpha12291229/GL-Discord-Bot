import discord
from discord.ext import commands



bot = commands.Bot(command_prefix='!')

class General(commands.Cog, name='General'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='server', help='Information about the server')
    async def server(self, ctx):
        name = str(ctx.guild.name)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        afkchannel = str(ctx.guild.afk_channel)

        embed = discord.Embed(
            title=name,
            #color=discord.Color.blue()
        )
        #embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server Id", value=id, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        embed.add_field(name="AFK Channel", value=afkchannel, inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='ping',help='Show everyone your wifi latency')
    async def ping(self, ctx):
        await ctx.send(f'Latency:{round(self.bot.latency * 1000)}ms')



def setup(bot):
    bot.add_cog(General(bot))