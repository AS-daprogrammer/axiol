import asyncio
import discord
from discord.ext import commands
import utils.vars as var
import utils.database as db
from utils.funcs import getprefix


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["extensions", "extentions", "addons"])
    @commands.has_permissions(administrator=True)
    async def plugins(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id}, {"_id":False}) #Getting guild's plugin document and removing the ID
        enabled_amount = len([keys for keys, values in GuildDoc.items() if values == True])
        total_amount = len(GuildDoc) -1 #Removing ID

        embed = discord.Embed(
        title="All available plugins",
        description="React to the respective emojis below to enable/disable them!",
        color=var.CMAIN
        ).set_footer(text=f"{enabled_amount}/{total_amount} plugins are enabled in this server")
        
        for i in GuildDoc:
            status = "Enabled" if GuildDoc.get(i) == True else "Disabled"
            embed.add_field(name=i, value=f"{var.PLUGINEMOJIS.get(i)} {status}", inline=False)

        botmsg = await ctx.send(embed=embed)
        for i in GuildDoc:
            await botmsg.add_reaction(var.PLUGINEMOJIS.get(i))
        
        def reactioncheck(reaction, user):
            return user == ctx.author and reaction.message == botmsg

        def enablecheck(reaction, user):
            if str(reaction.emoji) == var.ENABLE:
                return user == ctx.author and reaction.message == enabledbotmsg

        def disablecheck(reaction, user):
            if str(reaction.emoji) == var.DISABLE:
                return user == ctx.author and reaction.message == enabledbotmsg

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=reactioncheck, timeout=60.0)
                GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
                if str(reaction.emoji) in var.PLUGINEMOJIS.values():
                    await botmsg.remove_reaction(str(reaction.emoji), ctx.author)
                    plugin_type = list(var.PLUGINEMOJIS.keys())[list(var.PLUGINEMOJIS.values()).index(str(reaction.emoji))]

                    embed = discord.Embed(
                    title=f"{plugin_type} Plugin",
                    )
                    if GuildDoc.get(plugin_type) == True:
                        embed.description=f"{var.ENABLE} {plugin_type} is currently enabled"
                        embed.color=var.CGREEN
                        enabledbotmsg = await ctx.send(embed=embed)
                        await enabledbotmsg.add_reaction(var.DISABLE)

                        await self.bot.wait_for('reaction_add', check=disablecheck)
                        newdata = {"$set":{
                            plugin_type: False
                        }}
                        db.PLUGINS.update_one(GuildDoc, newdata)

                        embed.title=f"{plugin_type} disabled"
                        embed.description=f"{var.DISABLE} {plugin_type} extension has been disabled"
                        embed.color=var.CRED
                        await enabledbotmsg.edit(embed=embed)
                        await enabledbotmsg.clear_reactions()

                    else:
                        embed.description=f"{var.DISABLE} {plugin_type} is currently disabled"
                        embed.color = var.CRED
                        enabledbotmsg = await ctx.send(embed=embed)
                        await enabledbotmsg.add_reaction(var.ENABLE)

                        await self.bot.wait_for('reaction_add', check=enablecheck)
                        newdata = {"$set":{
                            plugin_type: True
                        }}
                        db.PLUGINS.update_one(GuildDoc, newdata)

                        embed.title=f"{plugin_type} enabled"
                        embed.description=f"{var.ENABLE} {plugin_type} extension has been enabled"
                        embed.color=var.CGREEN
                        await enabledbotmsg.edit(embed=embed)
                        await enabledbotmsg.clear_reactions()

                        #Since welcome is not enabled by default ->
                        #The time plugin is enabled, there is no information avaialable in the db ->
                    #Hence we ask for the welcome channel and insert the data
                    if str(reaction.emoji) == "👋" and db.WELCOME.find_one({"_id": ctx.guild.id}) is None:

                        embed = discord.Embed(
                        title="Send the welcome channel where I can greet members!",
                        description="Since this is the first time this plugin is being enabled, I need to know where I am supposed to greet new members :D",
                        color=var.CBLUE
                        ).set_footer(text="The next message which you will send will become the welcome channel, make sure that the Channel/ChannelID is valid other wise this won't work"
                        )
                        await ctx.send(embed=embed)
                        def messagecheck(message):
                            return message.author == ctx.author and message.channel.id == ctx.channel.id
                        usermsg = await self.bot.wait_for('message', check=messagecheck)
                        chid = int(usermsg.content.strip("<>#"))

                        db.WELCOME.insert_one({

                            "_id":ctx.guild.id,
                            "channelid":chid,
                            "greeting": "Hope you enjoy your stay here :)",
                            "image": "https://image.freepik.com/free-vector/welcome-sign-neon-light_110464-147.jpg",
                            "assignroles": []
                        })
                        successembed = discord.Embed(
                        title="Welcome greeting successfully setted up",
                        description=f"{var.ACCEPT} New members will now be greeted in {self.bot.get_channel(chid).mention}!",
                        color=var.CGREEN
                        ).add_field(name="To configure further", value=f"`{getprefix(ctx)}help welcome`")
                        
                        await ctx.send(embed=successembed)
                
                    #Same with verification
                    if str(reaction.emoji) == var.ACCEPT and db.VERIFY.find_one({"_id": ctx.guild.id}) is None:

                        embed = discord.Embed(
                        title="Send the verify channel",
                        description="Since this is the first time this plugin is being enabled, I need to know where I am supposed to verify new members :D",
                        color=var.CBLUE
                        ).set_footer(text="The next message which you will send will become the verify channel, make sure that the channel/channelID is valid other wise this won't work")
                        botmsg = await ctx.send(embed=embed)

                        def messagecheck(message):
                            return message.author == ctx.author and message.channel.id == ctx.channel.id

                        usermsg = await self.bot.wait_for('message', check=messagecheck)
                        chid = int(usermsg.content.strip("<>#"))
                        NVerified = await ctx.guild.create_role(name="Not Verified", colour=discord.Colour(0xa8a8a8))
                        await botmsg.clear_reactions()

                        embed.title="Processing..."
                        embed.description="Setting up everything, just a second"
                        embed.set_footer(text="Creating the 'Not Verified' role and setting up proper permissions")
                        await botmsg.edit(embed=embed)
                        for i in ctx.guild.text_channels:
                            await i.set_permissions(NVerified, view_channel=False)
                        await self.bot.get_channel(chid).set_permissions(NVerified, view_channel=True, read_message_history=True)
                        await self.bot.get_channel(chid).set_permissions(ctx.guild.default_role, view_channel=False)
                        db.VERIFY.insert_one({
                            
                            "_id":ctx.guild.id,
                            "type": "command",
                            "channel": chid, 
                            "roleid": NVerified.id
                        })
                        successembed = discord.Embed(
                        title="Verification successfully setted up",
                        description=f"{var.ACCEPT} New members would need to verify in {self.bot.get_channel(chid).mention} to access other channels!",
                        color=var.CGREEN
                        ).add_field(name="To configure further", value=f"`{getprefix(ctx)}help verification`"
                        ).set_footer(text="Default verification type is command")
                        
                        await ctx.send(embed=successembed)

            except asyncio.TimeoutError:
                await botmsg.clear_reactions()
                


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def prefix(self, ctx):
        embed = discord.Embed(
        title="Prefix :D that's the way you control me aye!",
        description=f"The prefix for this server is\n```{getprefix(ctx)}```\nWanna change it? React to the {var.SETTINGS} emoji below!",
        color=var.CMAIN
        )
        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction(var.SETTINGS)

        def reactioncheck(reaction, user):
            return user == ctx.author and reaction.message == botmsg

        await self.bot.wait_for('reaction_add', check=reactioncheck)
        await ctx.send(embed=discord.Embed(
                    description="Next message which you will send will become the prefix :eyes:\n"+
                    f"To cancel it enter\n```{getprefix(ctx)}cancel```",
                    color=var.CORANGE
                    ).set_footer(text="Automatic cancellation after 1 minute")
                    )
        await botmsg.clear_reactions()

        def messagecheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        try:
            usermsg = await self.bot.wait_for('message', check=messagecheck, timeout=60.0)

            if usermsg.content == getprefix(ctx)+"cancel":
                await ctx.send("Cancelled prefix change.")
                
            elif usermsg.content == var.DEFAULT_PREFIX:
                db.PREFIXES.delete_one({"serverid": ctx.guild.id})
                await ctx.send(f"Changed your prefix to the default one\n```{var.DEFAULT_PREFIX}```")

            elif getprefix(ctx) == var.DEFAULT_PREFIX:
                db.PREFIXES.insert_one({"_id": db.PREFIXES.estimated_document_count()+1, "serverid": ctx.guild.id, "prefix": usermsg.content})
                await ctx.send(f"Updated your new prefix, it's\n```{usermsg.content}```")

            else:
                oldprefix = db.PREFIXES.find_one({"serverid": usermsg.guild.id})
                newprefix = {"$set": {"serverid": usermsg.guild.id, "prefix": usermsg.content}}
                
                db.PREFIXES.update_one(oldprefix, newprefix)
                await ctx.send(f"Updated your new prefix, it's\n```{usermsg.content}```")

        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to enter your new prefix {ctx.author.mention} ;-;")


def setup(bot):
    bot.add_cog(Settings(bot))