import discord
from discord.ext import commands
import aiohttp
import sys
import time
import googletrans
import functools
import datetime
import pytz


class utility:
    def __init__(self, bot):
	    self.bot = bot


    @commands.command(hidden=True)
    @commands.has_permissions(manage_guild = True)
    async def addemoji(self, ctx, name, id):
	    '''add new emojis by id'''
	    url = f"https://cdn.discordapp.com/emojis/{id}"
	    async with self.bot.session.get(url) as resp:
			    image = await resp.read()
	    done = await ctx.guild.create_custom_emoji(name = name, image = image)
	    await ctx.send("Emoji {} created!".format(done))

    @commands.command(hidden=True)
    @commands.has_permissions(manage_guild = True)
    async def createemoji(self, ctx, name, url):
        '''add new emojis by url'''
        async with self.bot.session.get(url) as resp:
		        image = await resp.read()
        done = await ctx.guild.create_custom_emoji(name = name, image = image)
        await ctx.send("Emoji {} created!".format(done))
		
    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
       if member is None:
          embed=discord.Embed(title="No mention!", description="Please mention a user to view his profile!", color=0xff0000)
          await ctx.send(embed=embed)
       else:
          embed = discord.Embed(title=f"{member}'s profile picture", color=0xeee657)
          embed.set_image(url=member.avatar_url)
          await ctx.send(embed=embed)

    @commands.command()
    async def code(self, ctx, *, msg):
           """Write text in code format."""
           await ctx.message.delete()
           await ctx.send("```" + msg.replace("`", "") + "```")

       
    @commands.command()
    async def echo(self, ctx, *, content:str):
           await ctx.send(content)
           await ctx.message.delete()
		
    # @commands.command()
    # async def hello(self, ctx):
    #        """*hello
    #        A command that will respond with a random greeting.
    #        """
    #        choices = ('Hey!', 'Hello!', 'Hi!', 'Hallo!', 'Bonjour!', 'Hola!')
    #        await ctx.send(choice(choices))
    
    @commands.command(aliases=['platform'],hidden=True)
    async def plat(self,ctx):
           await ctx.send('Running on ' + sys.platform)
	
    @commands.command(name='members',hidden=True)
    async def members(self, ctx):
        server = ctx.guild
        for member in server.members:
            await ctx.send(member)

    @commands.command(name='roles',hidden=True)
    async def _members(self, ctx):
        server = ctx.guild
        for role in server.roles:
            await ctx.send(role)

    @commands.command(name='member',hidden=True)
    async def roles(self, ctx):
        server = ctx.guild
        list = []
        for member in server.members:
            list.append(member.name)
        embed = discord.Embed(name =    'Members', description =    str(list) ,colour =    discord.Colour.green())
        await ctx.send(embed=embed)

    @commands.command(name='rolee',hidden=True)
    async def _roles(self, ctx):
        server = ctx.guild
        list = []
        for role in server.roles:
            list.append(role.name)
        embed = discord.Embed(name =    'Roles', description =    str(list) ,colour =    discord.Colour.green())
        await ctx.send(embed=embed)

    @commands.command(name='pingme')
    async def pingme(self, ctx):
        embed=discord.Embed(description =    ctx.author.mention,colour =    discord.Colour.red())
        await ctx.send(embed=embed)
	

    # @commands.command()
    # @commands.has_permissions(manage_guild = True)
    # async def changeprefix(self, ctx, prefix):
	#     '''Change prefix of your bot in guild'''
	#     await self.bot.db.config.update_one({"gid" : ctx.guild.id}, {"$set" : {"prefix" : prefix}}, upsert = True)
	#     await ctx.send(f"New Prefix of {ctx.guild.name} is {prefix}, You can also change it again by doing {prefix}changeprefix <newprefix>.")

    @commands.command()
    async def datetime(self, ctx, tz=None):
        """Get the current date and time for a time zone or UTC."""
        now = datetime.datetime.now(tz=pytz.UTC)
        all_tz = 'https://github.com/Techarpan/garena/blob/master/data/timezones.json'
        if tz:
            try:
                now = now.astimezone(pytz.timezone(tz))
            except:
                em = discord.Embed(color=discord.Color.red())
                em.title = "Invalid timezone"
                em.description = f'Please take a look at the [list]({all_tz}) of timezones.'
                return await ctx.send(embed=em)
        await ctx.send(f'It is currently {now:%A, %B %d, %Y} at {now:%I:%M:%S %p}.')

    @commands.group(invoke_without_command=True)
    async def isit(self, ctx):
        '''A command group to see the number of days until a holiday'''
        await ctx.send(f'`{ctx.prefix}isit halloween` Find the number of days until this spooky holiday!\n`{ctx.prefix}isit christmas` Are you naughty or nice?\n`{ctx.prefix}isit newyear` When is next year coming already?')

    @commands.group(invoke_without_command=True)
    async def whenis(self, ctx):
        '''A command group to see the number of days until a holiday'''
        await ctx.send(f'`{ctx.prefix}whenis halloween` Find the number of days until this spooky holiday!')


    @isit.command()
    async def halloween(self, ctx):
        now = datetime.datetime.now()
        h = datetime.datetime(now.year, 10, 31)
        if now.month > 10:
            h = datetime.datetime(now.year + 1, 10, 31)
        until = h - now
        if now.month == 10 and now.day == 31:
            await ctx.send('It is Halloween! :jack_o_lantern: :ghost:')
        else:
            if until.days + 1 == 1:
                return await ctx.send('No, tomorrow is Halloween!')
            await ctx.send(f'No, there are {until.days + 1} more days until Halloween.')

    @whenis.command(aliases=['hallo','hw'])
    async def whalloween(self, ctx):
        now = datetime.datetime.now()
        h = datetime.datetime(now.year, 10, 31)
        if now.month > 10:
            h = datetime.datetime(now.year + 1, 10, 31)
        until = h - now
        if now.month == 10 and now.day == 31:
            await ctx.send('It is Halloween! :jack_o_lantern: :ghost:')
        else:
            if until.days + 1 == 1:
                await ctx.send("Halloween is on 31st of October")
                return await ctx.send('One more day remaining for halloween!')
            await ctx.send("Halloween is on 31st of October")
            await ctx.send(f'That is {until.days + 1} days remaining for Halloween.')

    @commands.command(name='translate')
    async def _translate(self, ctx, text, *, langs=""):
        """: Translate things you don't understand
        """
    # We want to search things like `from` and `to` in our "text" so the command would be like
    # {prefix}translate "this" `from` thislang `to` thatlang
    # if you don't provide anything then it automatically detects language and translates it to English
    # Make sure text is in " "
        def convert(s: str) -> dict:
            a = s.lower().split()
            res = {
                a[i]: a[i + 1]
                for i in range(len(a)) if a[i] in ("from", "to")
            }
            res["from"] = res.get("from") or "auto"
            res["to"] = res.get("to") or "en"
            return res

        try:
            langdict = convert(langs)
        except IndexError:
            raise commands.BadArgument("Invalid language format.")
        translator = googletrans.Translator()
        tmp = functools.partial(
            translator.translate,
            text,
            src=langdict["from"],
            dest=langdict["to"])
        try:
            async with ctx.typing():
                res = await self.bot.loop.run_in_executor(None, tmp)
        except ValueError as e:
            raise commands.BadArgument(e.args[0].capitalize())
        await ctx.send(res.text.replace("@", "@\u200b"))



def setup(bot):
    bot.add_cog(utility(bot))