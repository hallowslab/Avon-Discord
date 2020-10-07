import logging
#pylint: disable=unused-import
import youtube_dl
import discord
from discord.ext import commands
from Avon import config
from Avon.ping_host import ping


logger = logging.getLogger("Avon-Discord")


@commands.command()
@commands.has_role("Admin")
async def close(ctx):
    """
    Closes the bot connection
    """
    await ctx.send("Logging out!")
    await ctx.bot.logout()


@commands.command()
@commands.has_role("Admin")
async def kick(ctx, member: discord.Member, reason: str = None):
    """
    kicks the member and specifies reason
    """
    reason = "No reason defined" if reason is None else reason
    await ctx.send("Kicking user %s, reason: %s" % (member, reason))
    await member.kick(reason=reason)


@commands.command()
@commands.has_role("Admin")
async def ban(ctx, member: discord.Member, reason: str = None):
    """
    Bans the member and specifies reason
    """
    reason = "No reason defined" if reason is None else reason
    await ctx.send("Kicking user %s, reason: %s" % (member, reason))
    # I'm not sure why the default for delete_message_days is 1
    # So i just bumped it up to 2 (makes perfect sense)
    await member.ban(reason=reason, delete_message_days=2)


@commands.command()
@commands.has_role("Admin")
async def testspeed(ctx, url: str):
    """
    Runs google page speed insights on the url
    """
    # TODO: unfinished
    await ctx.send("Running page speed insights on %s" % url)


@commands.command()
@commands.has_role("Admin")
async def sysping(ctx, host: str):
    """
    Pings a host trough system calls
    """
    await ctx.send("Pinging host %s" % host)
    if ping(host):
        await ctx.send("Host is online")
    else:
        await ctx.send("Host seems to be down, or refusing ping requests")


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
