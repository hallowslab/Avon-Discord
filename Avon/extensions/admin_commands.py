import logging
#pylint: disable=unused-import
import youtube_dl
import discord
from discord.ext import commands
from Avon import config
from Avon.ping_host import ping


logger = logging.getLogger("Avon-Discord")


@commands.command()
async def close(ctx):
    """
    Closes the bot connection
    """
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        await ctx.send("Logging out!")
        await ctx.bot.logout()
    else:
        await ctx.send("You do not have permissions to execute that!")


@commands.command()
async def kick(ctx, member: discord.Member, reason: str = None):
    """
    kicks the member and specifies reason
    """
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        reason = "No reason defined" if reason is None else reason
        await ctx.send("Kicking user %s, reason: %s" % (member, reason))
        await member.kick(reason=reason)
    else:
        await ctx.send("You do not have permissions to execute that!")


@commands.command()
async def ban(ctx, member: discord.Member, reason: str = None):
    """
    kicks the member and specifies reason
    """
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        reason = "No reason defined" if reason is None else reason
        await ctx.send("Kicking user %s, reason: %s" % (member, reason))
        # I'm not sure why the default for delete_message_days is 1
        # So i just bumped it up to 2 (makes perfect sense)
        await member.ban(reason=reason, delete_message_days=2)
    else:
        await ctx.send("You do not have permissions to execute that!")


@commands.command()
async def testspeed(ctx, url: str):
    """
    kicks the member and specifies reason
    """
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        # TODO: unfinished
        await ctx.send("Running page speed insights on %s" % url)
    else:
        await ctx.send("You do not have permissions to execute that!")


@commands.command()
async def sysping(ctx, host: str):
    """
    kicks the member and specifies reason
    """
    if str(ctx.message.author.id) == config.access_keys["master_id"]:
        await ctx.send("Pinging host %s" % host)
        if ping(host):
            await ctx.send("Host is online")
        else:
            await ctx.send("Host seems to be down, or refusing ping requests")
    else:
        await ctx.send("You do not have permissions to execute that!")


def setup(bot):
    """
    Function to load commands as a bot extension
    """
    cmds = [
        close,
        kick,
        ban,
        testspeed,
        sysping
    ]
    for command in cmds:
        bot.add_command(command)
