import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='!')

class ToDo(commands.Cog, name='Todo'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add', help='Add Task to ToDo List')
    async def add(self, ctx, task):
        id = str(ctx.author.id)

        a_file = open("./cogs/todo.json", "r")
        data = json.load(a_file)
        a_file.close()
        
        if id in data:
            data[id]['todo'].append(task)
        else:
            data[id] = {}
            data[id]['todo']=[task]
            data[id]['done']=[]

        a_file = open("./cogs/todo.json", "w")
        json.dump(data, a_file)
        a_file.close()

        await ctx.send(f'{task} has been added to ToDo List')

    @commands.command(name='done', help='Mark Task as Done')
    async def done(self, ctx, task):
        id = str(ctx.author.id)

        a_file = open("./cogs/todo.json", "r")
        data = json.load(a_file)
        a_file.close()
        
        if id in data:
            if task in data[id]['todo']:
                data[id]['todo'].remove(task)
                data[id]['done'].append(task)
                output = f'{task} has been shifted to Done List'
            else:
                output = f'{task} cannot be found'
        else:
            output = f'{ctx.author} cannot be found'

        a_file = open("./cogs/todo.json", "w")
        json.dump(data, a_file)
        a_file.close()

        await ctx.send(output)
    
    @commands.command(name='delete', help='Delete Task from ToDo List !delete list task')
    async def delete(self, ctx, list, task):
        id = str(ctx.author.id)
        list = str.lower(list)

        a_file = open("./cogs/todo.json", "r")
        data = json.load(a_file)
        a_file.close()

        if id in data:
            if task in data[id][list]:
                data[id][list].remove(task)
                a_file = open("./cogs/todo.json", "w")
                json.dump(data, a_file)
                a_file.close()
                output = f'{task} has been deleted from {list} List'
            else:
                output = f'{task} cannot be found'    
        else: 
            output = f'{ctx.author} cannot be found'
        
        await ctx.send(output)

    @commands.command(name='todo', help='Prints Users ToDo List')
    async def todo(self, ctx):
        id = str(ctx.author.id)

        a_file = open("./cogs/todo.json", "r")
        data = json.load(a_file)
        a_file.close()

        if id in data:
            embed = discord.Embed(title="ToDo List")

            if data[id]['todo']!=[]:
                todolist = '\n'.join([x for x in data[id]['todo']])
                embed.add_field(name="Todo", value=f"{''.join(todolist)}")

            if data[id]['done']!=[]:
                donelist = '\n'.join([x for x in data[id]['done']])
                embed.add_field(name="Done", value=f"{''.join(donelist)}")

            output = embed 
        else: 
            embed = discord.Embed(title="ToDo List")
            embed.add_field(name="ERROR",value=f'{ctx.author} cannot be found')
            output = embed 
        
        await ctx.send(embed=output)

def setup(bot):
    bot.add_cog(ToDo(bot))
