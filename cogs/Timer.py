import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime

def get_expire_time(minutes: int) -> datetime.datetime:
    """ get expire time after minutes from now
    args
        minutes: int
    return
        expire_time: datetime.datetime
    """
    now = datetime.datetime.now()
    expire_time = now + datetime.timedelta(minutes=minutes)
    return expire_time

bot = commands.Bot(command_prefix='!')

sched = AsyncIOScheduler()
sched.start()

class Timer(commands.Cog, name="Timer"):
    def __init__(self, bot):
        self.bot = bot    

    @commands.command(name='start', help="Start timer recommended: '!start 25 5'")
    async def start(self, ctx, work_time: int=25, break_time: int=5):
        """ Start pomodoro timer
        Action:
            Start break_time timer after work_time timer
        Args:
            work_time : work timer (minute)
            break_time : break timer after work_time (minute)
        """

        if sched.get_job(job_id=str(ctx.author.id)) != None :
            await ctx.channel.send(
            f"```css\n[⚠️Pomodoro timer already working!]\n - stop command : !stop```")
            return

        

        async def break_schedule(ctx, work_time, break_time):
            print('Enter break schedule')
            await ctx.channel.send(
                f"{ctx.author.mention}```css\n[🔥Break time end!] Let's work :)```")
            work_expire_time = get_expire_time(work_time)
            print(work_expire_time)
            sched.add_job(work_schedule, 'date', run_date=work_expire_time, args=[ctx,work_time, break_time],id=str(ctx.author.id))
            pass

        async def work_schedule(ctx, work_time, break_time):
            print('Enter work schedule')
            await ctx.channel.send(
                f"{ctx.author.mention}```css\n[🏁Work time end!] Let's break :)```")
            break_expire_time = get_expire_time(break_time)
            print(break_expire_time)
            sched.add_job(break_schedule, 'date', run_date=break_expire_time, args=[ctx,work_time, break_time],id=str(ctx.author.id))
            pass

        work_expire_time = get_expire_time(work_time)
        sched.add_job(work_schedule, 'date', run_date=work_expire_time, args=[ctx,work_time, break_time],id=str(ctx.author.id))

        await ctx.channel.send(
            f"```css\n[Work {work_time}min, Break {break_time}min] Pomodoro Timer START.\n - stop command : !stop```")


    @commands.command(name='stop', help="Stop timer")
    async def stop(self, ctx):
        """ Stop pomodoro timer
        Action:
            Stop pomodoro timer
        """
        sched.remove_job(job_id=str(ctx.author.id))
        await ctx.channel.send(
            f"```css\nPomodoro Timer STOP.\n - start command : !start [work_min] [break_min]```")


def setup(bot):
    bot.add_cog(Timer(bot))
