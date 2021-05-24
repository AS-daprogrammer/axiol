import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, invoke_without_command=True)
    async def help(self, ctx):

        embed = discord.Embed(title="Axiol Help", description=f"Either enter the sub command or react to the emojis below!", color=var.CMAIN)
        embed.add_field(name=getprefix(ctx)+"help levels", value=f"Leveling help {var.LVL}", inline=False)
        embed.add_field(name=getprefix(ctx)+"help mod", value="Moderation help 🔨", inline=False)
        embed.add_field(name=getprefix(ctx)+"help rr", value="Reaction role help ✨", inline=False)
        embed.add_field(name=getprefix(ctx)+"source", value="My Github source code!", inline=False)
        embed.add_field(name=getprefix(ctx)+"suggest `<youridea>`",value="Suggest an idea which will be sent in the official [Axiol Support Server](https://discord.gg/KTn4TgwkUT)!", inline=False)
        embed.add_field(name=getprefix(ctx)+"invite",value="[Invite link for the bot!](https://discord.com/api/oauth2/authorize?client_id=843484459113775114&permissions=8&scope=bot)", inline=False)
        embed.add_field(name=getprefix(ctx)+"embed `<#channel>`",value="Generate an embed!", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
        helpmsg = await ctx.send(embed=embed)
        await helpmsg.add_reaction(var.LVL)
        await helpmsg.add_reaction('🔨')
        await helpmsg.add_reaction('✨')

        #Embeds
        levelembed = discord.Embed(title="Ah yes leveling, MEE6 who?", color=var.CMAIN)
        levelembed.add_field(name=getprefix(ctx)+"levels", value="Setup and configure leveling!", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"rank `<user>`", value="Shows server rank of the user, user id or user mention can be used to check ranks, user field is optional for checking rank of yourself.", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"leaderboard", value="Shows server leaderboard!", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"givexp `<user>` `<amount>`", value="Gives user more XP! For user either user can be mentioned or ID can be used", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"removexp `<user>` `<amount>`", value="Removes user more XP! For user either user can be mentioned or ID can be used", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"award", value="Setup awards for reaching certain amount of xp!", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"settings", value="Configure leveling settings! Only works for admins", inline=False)
        levelembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")

        modembed = discord.Embed(title="Moderation", description="What's better than entering a sweet little ban command?", color=var.CMAIN)
        modembed.add_field(name=getprefix(ctx)+"prefix", value="Check and change your server prefix!", inline=False)
        modembed.add_field(name=getprefix(ctx)+"ban `<reason>`", value="Bans a user until unbanned, reason is optional", inline=False)
        modembed.add_field(name=getprefix(ctx)+"unban", value="Unbans a banned user", inline=False)
        modembed.add_field(name=getprefix(ctx)+"kick `<reason>`", value="Kicks the user out of the server, reason is optional", inline=False)
        modembed.add_field(name=getprefix(ctx)+"mute", value="Assigns 'Muted' role to the user hence disabling their ability to send messages! If the role does not exist then I can make it on my own when the command is used!", inline=False)
        modembed.add_field(name=getprefix(ctx)+"unmute", value="Removes the 'Muted' role therefore lets the user send messages.", inline=False)
        modembed.add_field(name=getprefix(ctx)+"purge `<amount>`", value="Deletes the number of messages defined in the command from the channel", inline=False)
        modembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")

        rrembed = discord.Embed(title="Reaction Roles", color=var.CMAIN)
        rrembed.add_field(name=getprefix(ctx)+"rr `<messageid>` `<role>` `<emoji>`", value="Setup reaction roles in your server! For role either role ID or role ping can be used.", inline=False)
        rrembed.add_field(name=getprefix(ctx)+"removerr `<messageid>` `<emoji>`", value="Remove any existing reaction role.", inline=False)
        rrembed.add_field(name=getprefix(ctx)+"allrr", value="View all active reaction roles in the server!", inline=False)
        rrembed.add_field(name=getprefix(ctx)+"uniquerr `<messageid>`", value="Mark a message with unique reactions! Users would be able to react once hence take one role from the message.", inline=False)
        rrembed.add_field(name=getprefix(ctx)+"removeunique `<messageid>`", value="Unmark the message with unique reactions! Users would be able to react multiple times hence take multiple roles from the message.", inline=False)
        rrembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")


        def check(reaction, user):
            return user == ctx.author and reaction.message == helpmsg
      
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30.0)
                if str(reaction.emoji) == var.LVL:
                    await helpmsg.edit(embed=levelembed)
                    await helpmsg.remove_reaction(var.LVL, ctx.author)
                if str(reaction.emoji) == '🔨':
                    await helpmsg.edit(embed=modembed)
                    await helpmsg.remove_reaction('🔨', ctx.author)
                if str(reaction.emoji) == '✨':
                    await helpmsg.edit(embed=rrembed)
                    await helpmsg.remove_reaction('✨', ctx.author)
            except asyncio.TimeoutError:
                break


    @help.command(aliases=["level"])
    async def levels(self, ctx):
        levelembed = discord.Embed(title="Ah yes leveling, MEE6 who?", color=var.CMAIN)
        levelembed.add_field(name=getprefix(ctx)+"levels", value="Setup and configure leveling!", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"rank `<user>`", value="Shows server rank of the user, user id or user mention can be used to check ranks, user field is optional for checking rank of yourself.", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"leaderboard", value="Shows server leaderboard!", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"givexp `<user>` `<amount>`", value="Gives user more XP! For user either user can be mentioned or ID can be used", inline=False)
        levelembed.add_field(name=getprefix(ctx)+"removexp `<user>` `<amount>`", value="Removes user more XP! For user either user can be mentioned or ID can be used", inline=False)
        #levelembed.add_field(name=getprefix(ctx)+"award", value="Setup awards for reaching certain amount of xp!", inline=False)
        #levelembed.add_field(name=getprefix(ctx)+"settings", value="Configure leveling settings! Only works for admins", inline=False)
        levelembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
        await ctx.send(embed=levelembed)

    @help.command()
    async def mod(self, ctx):
        modembed = discord.Embed(title="Moderation", descriptio="What's better than entering a sweet little ban command?", color=var.CMAIN)
        modembed.add_field(name=getprefix(ctx)+"prefix", value="Check and change your server prefix!", inline=False)
        modembed.add_field(name=getprefix(ctx)+"ban `<reason>`", value="Bans a user until unbanned, reason is optional", inline=False)
        modembed.add_field(name=getprefix(ctx)+"unban", value="Unbans a banned user", inline=False)
        modembed.add_field(name=getprefix(ctx)+"kick `<reason>`", value="Kicks the user out of the server, reason is optional", inline=False)
        modembed.add_field(name=getprefix(ctx)+"mute", value="Assigns 'Muted' role to the user hence disabling their ability to send messages! If the role does not exist then I can make it on my own when the command is used!", inline=False)
        modembed.add_field(name=getprefix(ctx)+"unmute", value="Removes the 'Muted' role therefore lets the user send messages.", inline=False)
        modembed.add_field(name=getprefix(ctx)+"purge `<amount>`", value="Deletes the number of messages defined in the command from the channel", inline=False)
        modembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
        await ctx.send(embed=modembed)

    @help.command()
    async def rr(self, ctx):
        rrembed = discord.Embed(title="Reaction Roles", color=var.CMAIN)
        rrembed.add_field(name=getprefix(ctx)+"rr `<messageid>` `<role>` `<emoji>`", value="Setup reaction roles in your server! For role either role ID or role ping can be used.", inline=False)
        rrembed.add_field(name=getprefix(ctx)+"removerr `<messageid>` `<emoji>`", value="Remove any existing reaction role.", inline=False)
        rrembed.add_field(name=getprefix(ctx)+"allrr", value="View all active reaction roles in the server!", inline=False)
        rrembed.add_field(name=getprefix(ctx)+"uniquerr `<messageid>`", value="Mark a message with unique reactions! Users would be able to react once hence take one role from the message.", inline=False)
        rrembed.add_field(name=getprefix(ctx)+"removeunique `<messageid>`", value="Unmark the message with unique reactions! Users would be able to react multiple times hence take multiple roles from the message.", inline=False)

        await ctx.send(embed=rrembed)



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        
        embed = discord.Embed(title="Configure leveling for this server",
        color=var.CTEAL
        ).add_field(name=getprefix(ctx)+"blacklist `<#channel>`",value=f"Add the channel where you don't want users to gain xp.", inline=False
        ).add_field(name=getprefix(ctx)+"xp `<leastamount>` `<highestamount>`",value="Set the range between which users will be awarded with random xp", inline=False
        ).add_field(name=getprefix(ctx)+"maxlevel `<amount>`", value="Define the max level which can be achieved by a user", inline=False
        ).add_field(name=getprefix(ctx)+"alertchannel `<#channel>`", value="Define the channel where alerts will be sent for level ups!", inline=False
        ).add_field(name=getprefix(ctx)+"alertmessage `<message>`", value=f"Change the alert message! Use these values in between:\n[user] [xp] [level]\n Make sure to put them between square brackets!", inline=False
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))