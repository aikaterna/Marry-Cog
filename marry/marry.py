import discord
from discord.ext import commands
from .utils.dataIO import dataIO
import os


class Marry:
    """You can get married to a user by using !marry @someone"""

    def __init__(self, bot):
        self.bot = bot
        self.JSON = 'data/married/married.json'
        self.data = dataIO.load_json(self.JSON)

    @commands.command(pass_context=True)
    async def marry(self, ctx, user: discord.Member):
        server = ctx.message.server
        author1 = ctx.message.author.mention
        author = ctx.message.author.name
        if user.mention == author1:
            msg = 'You can\'t get married to yourself, crazy guy.'
            em0 = discord.Embed(description=msg, color=0XF23636)
            await self.bot.say(embed=em0)
        else:
                desc = ":ring:" + author + " *has proposed to* " + user.name + ":ring:"
                name = ":church:" + user.name + ",  Do you accept? :church:"
                em = discord.Embed(description=desc, color=0XF23636)
                em.add_field(name=name, value='Type yes to accept or no to decline.')
                await self.bot.say(embed=em)
                response = await self.bot.wait_for_message(author=user)

                if response.content.lower().strip() == "yes":
                    await self._create_author(server, ctx, user)
                    await self._create_user(server, ctx, user)
                    msg = ":heart: Congratulations " + author + " and " + user.name + " :heart:"
                    em1 = discord.Embed(description=msg, color=0XF23636)
                    await self.bot.say(embed=em1)
                    dataIO.save_json(self.JSON, self.data)
                else:
                    msg = "The proposal between " + author + " and " + user.name + " has been declined."
                    em2 = discord.Embed(description=msg, color=0XF23636)
                    await self.bot.say(embed=em2)

    @commands.command(pass_context=True)
    async def divorce(self, ctx, user: discord.Member):
        author = ctx.message.author.name
        server = ctx.message.server
        if user.mention == author:
            em0 = discord.Embed(description='You cant\'t divorce yourself, crazy guy!', color=0XF23636)
            await self.bot.say(embed=em0)
        else:
            if user.name in self.data[server.id]["user"][author]["married_to"]:
                await self._divorce(server, ctx, user)
                me = ctx.message.author.name
                msg = ':broken_heart:  ' + me + ' *has divorced* ' + user.name + ' :broken_heart:'
                em = discord.Embed(description=msg, color=0XF23636)
                await self.bot.say(embed=em)
            else:
                msg = 'You can\'t divorce that user because you aren\'t married to them.'
                em = discord.Embed(description=msg, color=0XF23636)
                await self.bot.say(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def mlist(self, ctx, user: discord.Member=None):
        '''Get a list of who someone is married to. Defaults to author.'''
        author = ctx.message.author
        server = ctx.message.server

        if user is None:
            user = author

        if server.id not in self.data:
            await self.bot.say("No marriages on this server yet.")
            return

        if user.name not in self.data[server.id]["user"]:
            await self.bot.say("That person isn't married to anyone.")
            return

        mlist = (list(self.data[server.id]["user"][user.name]["married_to"]))
        names = ', '.join(map(str, mlist))

        if not mlist:
            await self.bot.say("That person isn't married to anyone.")

        elif user.name not in self.data[server.id]["user"]:
            await self.bot.say("That person isn't married to anyone.")

        else:
            em = discord.Embed(description="", color=0XF23636)
            em.add_field(name='Married to:', value=names)
            await self.bot.say(embed=em)

    async def _create_author(self, server, ctx, user):
        author = ctx.message.author.name
        if server.id not in self.data:
            self.data[server.id] = {}
            dataIO.save_json(self.JSON, self.data)
        if "user" not in self.data[server.id]:
            self.data[server.id]["user"] = {}
            dataIO.save_json(self.JSON, self.data)
        if author not in self.data[server.id]["user"]:
            self.data[server.id]["user"][author] = {}
            dataIO.save_json(self.JSON, self.data)
        if "married_to" not in self.data[server.id]["user"][author]:
            self.data[server.id]["user"][author]["married_to"] = {}
            dataIO.save_json(self.JSON, self.data)
        if user.name not in self.data[server.id]["user"][author]["married_to"]:
            self.data[server.id]["user"][author]["married_to"][user.name] = {}
        dataIO.save_json(self.JSON, self.data)
            #if author in self.data[server.id]["user"]:
            #   self.data[server.id]["user"][author]["married_to"] = user.name
            #   dataIO.save_json(self.JSON, self.data)
            #else:
            #   self.data[server.id]["user"] = author
            #   self.data[server.id]["user"][author]["married_to"] = user.name
            #   dataIO.save_json(self.JSON, self.data)

    async def _create_user(self, server, ctx, user):
        author = ctx.message.author.name
        if server.id not in self.data:
            self.data[server.id] = {}
            dataIO.save_json(self.JSON, self.data)
        if "user" not in self.data[server.id]:
            self.data[server.id]["user"] = {}
            dataIO.save_json(self.JSON, self.data)
        if user.name not in self.data[server.id]["user"]:
            self.data[server.id]["user"][user.name] = {}
            dataIO.save_json(self.JSON, self.data)
        if "married_to" not in self.data[server.id]["user"][user.name]:
            self.data[server.id]["user"][user.name]["married_to"] = {}
            dataIO.save_json(self.JSON, self.data)
        if author not in self.data[server.id]["user"][user.name]["married_to"]:
            self.data[server.id]["user"][user.name]["married_to"][author] = {}
        dataIO.save_json(self.JSON, self.data)
            #if author in self.data[server.id]["user"]:
            #   self.data[server.id]["user"][author]["married_to"] = user.name
            #   dataIO.save_json(self.JSON, self.data)
            #else:
            #   self.data[server.id]["user"] = author
            #   self.data[server.id]["user"][author]["married_to"] = user.name
            #   dataIO.save_json(self.JSON, self.data)

    async def _divorce(self, server, ctx, user):
        author = ctx.message.author.name
        del self.data[server.id]["user"][author]["married_to"][user.name]
        del self.data[server.id]["user"][user.name]["married_to"][author]
        dataIO.save_json(self.JSON, self.data)


def check_folder():
    if not os.path.exists('data/married'):
        print('Creating data/married folder...')
        os.makedirs('data/married')


def check_file():
    f = 'data/married/married.json'
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, {})
        print('Creating default married.json...')


def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Marry(bot))
