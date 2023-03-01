import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

bot = commands.Bot(command_prefix='!')

class Admin(commands.Cog, name='Admin'):
    def __init__(self, bot):
        self.bot = bot

    #Ban Command
    @commands.command(name="ban", help="ban user")
    #check whether user has permissions
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason=None):
        if reason == None:
            reason = f"{member} banned by {ctx.author}"      
        message = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(message)
        await ctx.channel.send(f"Banned: {member.mention}")
        await member.ban(reason=reason)

    #Send message if user has missing permissions
    @ban.error
    async def ban_error(self,ctx,error):
        if isinstance(error, MissingPermissions):
            await ctx.send(":x: You don't have enough permission to kick members.")

    #Unban Command
    @bot.command(name="unban", help="unban user")
    async def unban(self, ctx, *, member):
        #Find all banned users
        banned_users = await ctx.guild.bans()

        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            
            #Search for banned user. If found, unban
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f"Unbanned: {user.mention}")

    @bot.command(name="mute", help="mute member")
    async def mute(ctx, member: discord.Member):
        await member.edit(mute=True)
        
    @bot.command(name="unmute", help="unmute member")
    async def unmute(ctx, member: discord.Member):
        await member.edit(mute=False)



def setup(bot):
    bot.add_cog(Admin(bot))
