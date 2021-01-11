from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord.ext.commands import has_role
import configparser
bot = commands.Bot(command_prefix='!')
conf = configparser.ConfigParser()
conf.read('./config.ini')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(datetime.now())
    print('------')


@bot.command()
async def embedtest(ctx):
    embed=discord.Embed(title="Verification", description="User Approval", color=0x00ff40)
    embed.set_author(name="Checkpoint Bot", url="https://github.com/crackwatchdev/cw-checkpoint")
    embed.set_thumbnail(url="https://images.vexels.com/media/users/3/130496/isolated/preview/e18487bd9492fb9ef6fd32b3bddb3abe-gavel-court-hammer-icon-by-vexels.png")
    embed.add_field(name="Username", value="namevariable", inline=True)
    embed.add_field(name="Age", value="agevariable", inline=True)
    embed.add_field(name="Status", value="Approved", inline=False)
    embed.set_footer(text="With ❤ from the CrackWatch Team")
    await ctx.send(embed=embed)
@bot.command()
async def verify(ctx):
    age = ctx.message.author.created_at
    now = datetime.now()
    elapsedTime = now - age
    required = timedelta(days = 20)
    ApprovedRole = discord.utils.get(ctx.message.guild.roles, name=conf.get('bot', 'ApprovedRole'))
    DeniedRole = discord.utils.get(ctx.message.guild.roles, name=conf.get('bot', 'DeniedRole'))
    if (elapsedTime > required):
        to_send = 'Passed verification.'
        await ctx.message.guild.system_channel.send(to_send)
        await ctx.message.author.add_roles(ApprovedRole)
        if DeniedRole in ctx.message.author.roles:
            await ctx.message.author.remove_roles(DeniedRole)
    else:
        to_send = 'Did not pass. Contact staff member.'
        await ctx.message.guild.system_channel.send(to_send)
        await ctx.message.author.add_roles(DeniedRole)
@bot.command()
@has_role(conf.get('bot', 'ModRole'))
async def approve(ctx, member : discord.Member, reason):
    ApprovedRole = discord.utils.get(ctx.message.guild.roles, name=conf.get('bot', 'ApprovedRole'))
    age = member.created_at
    await member.add_roles(ApprovedRole)
    if DeniedRole in ctx.message.author.roles:
        await ctx.message.author.remove_roles(DeniedRole)
    embed=discord.Embed(title="Verification", description="User Approval", color=0x00ff00)
    embed.set_author(name="Checkpoint Bot", url="https://github.com/crackwatchdev/cw-checkpoint")
    embed.set_thumbnail(url="https://images.vexels.com/media/users/3/130496/isolated/preview/e18487bd9492fb9ef6fd32b3bddb3abe-gavel-court-hammer-icon-by-vexels.png")
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="Age", value=age, inline=True)
    embed.add_field(name="Status", value="Approved", inline=True)
    embed.add_field(name="Reason", value=reason, inline=True)
    embed.add_field(name="Approved by", value=ctx.message.author.name, inline=True)
    embed.set_footer(text="With ❤ from the CrackWatch Team")
    await ctx.message.guild.system_channel.send(embed=embed)
@bot.event
async def on_member_join(member):
    guild = member.guild
    age = member.created_at
    now = datetime.now()
    elapsedTime = now - age
    required = timedelta(days = 20)
    ApprovedRole = discord.utils.get(member.guild.roles, name=conf.get('bot', 'ApprovedRole'))
    DeniedRole = discord.utils.get(member.guild.roles, name=conf.get('bot', 'DeniedRole'))
    if (elapsedTime > required) is True:
        embed=discord.Embed(title="Verification", description="User Approval", color=0x00ff00)
        embed.set_author(name="Checkpoint Bot", url="https://github.com/crackwatchdev/cw-checkpoint")
        embed.set_thumbnail(url="https://images.vexels.com/media/users/3/130496/isolated/preview/e18487bd9492fb9ef6fd32b3bddb3abe-gavel-court-hammer-icon-by-vexels.png")
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="Age", value=age, inline=True)
        embed.add_field(name="Status", value="Approved", inline=True)
        embed.add_field(name="Reason", value="Age over 20 days.", inline=True)
        embed.set_footer(text="With ❤ from the CrackWatch Team")
        await guild.system_channel.send(embed=embed)
        await member.add_roles(ApprovedRole)
    else:
        embed=discord.Embed(title="Verification", description="User Approval", color=0xff0000)
        embed.set_author(name="Checkpoint Bot", url="https://github.com/crackwatchdev/cw-checkpoint")
        embed.set_thumbnail(url="https://images.vexels.com/media/users/3/130496/isolated/preview/e18487bd9492fb9ef6fd32b3bddb3abe-gavel-court-hammer-icon-by-vexels.png")
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="Age", value=age, inline=True)
        embed.add_field(name="Status", value="Denied", inline=True)
        embed.add_field(name="Reason", value="Age under 20 days. Contact a staff memeber.", inline=True)
        embed.set_footer(text="With ❤ from the CrackWatch Team")
        await guild.system_channel.send(embed=embed)
        await member.add_roles(DeniedRole)


bot.run(conf.get('bot', 'token'))
