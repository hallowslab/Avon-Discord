import logging
import discord
from discord.ext import commands


logger = logging.getLogger("Avon-Discord")


@commands.command()
async def dev_help(ctx, arg: str):
    """
    Embeds a message with help of provided method
    """
    title = "help(%s)" % arg
    embed_msg = discord.Embed(title=title, description="Shows the help for the provided module or function")
    ctx_methods = [method for method in dir(ctx) if not method.startswith("_")]
    msg_size = len(embed_msg.title) + len(embed_msg.description)
    for method in ctx_methods:
        reference = getattr(ctx, method, None).__doc__
        # Cut some of the description to avoid going over character limit
        reference = reference[:60] + "..." if reference is not None else reference
        ref_len = 4 if reference is None else len(reference)
        msg_size = msg_size + ref_len + len(method)
        embed_msg.add_field(name=method, value=reference, inline=False)
    logger.debug("lenght of message: %s", msg_size)
    await ctx.send(embed=embed_msg)


@commands.command()
async def dev_dir(ctx, arg: str):
    # I'm trying to make it possible to dir(ctx.something.something....)
    # main = ctx
    # if "." in arg:
    #     main = arg.rsplit(".", 1)
    #     logger.debug("main => %s" % main)
    #     arg = main[1]
    #     logger.debug("arg => %s" % arg)
    #     main = main[0]
    #     logger.debug("main => %s" % main)
    ref = ctx if arg == "ctx" else getattr(ctx, arg, None)
    logger.debug("ref => %s" % ref)
    if ref is None:
        await ctx.send("%s is not defined" % arg)
        return
    methods = [method for method in dir(ref) if not method.startswith("_")]
    if len(methods) == 0:
        await ctx.send("No methods found")
        return
    title = "dir(%s)" % arg
    embed_msg = discord.Embed(title=title, description="Shows the methods for the provided function/module")
    for method in methods:
        m_value = "%s()" % method
        embed_msg.add_field(name=method, value=m_value, inline=False)
    await ctx.send(embed=embed_msg)


def setup(bot):
    """
    Function to load commands as a bot extension
    """
    cmds = [
        dev_help,
        dev_dir
    ]
    for command in cmds:
        bot.add_command(command)
