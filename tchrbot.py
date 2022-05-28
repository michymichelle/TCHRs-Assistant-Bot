import discord
from discord.ext import commands
import gspread
from google.oauth2.service_account import Credentials
## Sources used listed in README.md

## Set the prefix to call all bot commands with
client = commands.Bot(command_prefix = '.')


## Return message to show bot is ready
@client.event
async def on_ready():
    print('Bot is ready.')


## Return ping latency
@client.command()
async def ping(ctx):
    await ctx.send(f'PongPongPong! @{round(client.latency*1000)}ms')


## Define the pay for different ranges of points
def payrange(points: int):
    if 28000 <= points < 32000:
        return (points*1000)/115
    elif 32000 <= points < 38000:
        return (points*1050)/115
    elif 38000 <= points < 47000:
        return (points*1150)/115
    elif 47000 <= points < 60000:
        return (points*1300)/115
    elif 60000 <= points < 80000:
        return (points*1500)/115
    elif 80000 <= points < 110000:
        return (points*1750)/115
    elif 110000 <= points < 150000:
        return (points*1850)/115
    elif 150000 <= points:
        return (points*2000)/115
    elif 28000 > points:
        return False


## Call payrange into paycheck function, calculate paycheck
@client.command(name='paycheck',aliases=['check','pcheck','pay','paycalculator'])
async def paycheck(context, points: int):
    if not False:
        pay = round(payrange(points))
        result = ("Your calculated paycheck is ${:,} for {:,} points.".format(pay, points))
        await context.send(result)
    # If below minimum points, return message
    if 28000 > points:
        await context.send("It appears you don't have enough points yet! The minimum is only 28,000 points a week!")


## Return top 10 players of the previous week (most points gained)
@client.command(name='crowns',aliases=['t10wk','toptenweek','top10week','top10weekly'])
async def sheet(context):
    # Connect Google services to .json file, contains authorization
    gc = gspread.service_account(filename='tchrs-assistant-c68f03d47663.json')
    # Specify Google spreadsheet file
    sh = gc.open_by_key("16nedbH2_k0It2yHbmRWOwSe9dYTjzG9x652XEdDcoA8")
    # Specifiy specific worksheet
    worksheet = sh.worksheet("Week 47 Points&Pay")
    # Create an embed
    toptenEmbed = discord.Embed(title='Last Week\'s Top 10 Racers', description='Who were TCHR\'s highest-achieving racers of the week?', color=0xffff42)
    # Add 10 new fields in embed, going down each row of two columns, return name and points
    i = 0
    for i in range(10):
        toptenEmbed.add_field(name="#"+str(i+1)+": "+worksheet.acell('G'+str((i+1)+1)).value, value='Total points gained: '+worksheet.acell('D'+str((i+1)+1)).value, inline=False)
    toptenEmbed.set_footer(text='Top 10 from Week 47. Week 48\'s competition currently ongoing. Aliases: .topten, .t10, .topten, .crowns')
    await context.send(embed=toptenEmbed)


## Return specified number of current top-ranking players
@client.command(name='top',aliases=['topnow','current','t'])
async def sheet(context, number: int):
    gc = gspread.service_account(filename='tchrs-assistant-c68f03d47663.json')
    sh = gc.open_by_key("16nedbH2_k0It2yHbmRWOwSe9dYTjzG9x652XEdDcoA8")
    cworksheet = sh.worksheet("Week 48 Points&Pay")
    lastupdate=cworksheet.acell('I1').value
    currenttopEmbed = discord.Embed(title='CURRENT Top '+str(number)+' Racers: ('+lastupdate+')', description=f'Who is CURRENTLY leading in the top '+str(number)+' this week?', color=0x7ffc03)
    i = 0
    for i in range(number):
        currenttopEmbed.add_field(name="#"+str(i+1)+": "+cworksheet.acell('C'+str((i+1)+1)).value, value='Total points gained: '+cworksheet.acell('D'+str((i+1)+1)).value, inline=False)
    currenttopEmbed.set_footer(text='This is the current top '+str(number)+'. Use .top10weekly for the weekly leaderboard. http://tinyurl.com/TCHRteam')
    await context.send(embed=currenttopEmbed)


## Returns spreadsheet link via direct command anywhere in server
@client.command(name='sheet', aliases=['link', 'sheetlink', 'spreadsheet'])
async def sheet(context):
    myEmbed = discord.Embed(title='TCHR Spreadsheet Link', description='With this sheet, you can find how many points you have and how much you might get paid this week!', color=0x99ffcc)
    myEmbed.add_field(name="Spreadsheet Link",value="http://tinyurl.com/TCHRteam",inline=False)
    myEmbed.set_footer(text='Created by @michymichelle')
    myEmbed.set_author(name='Michy')
    await context.message.channel.send(embed=myEmbed)


## Returns spreadsheet link via mention of keywords in specific channel
@client.event
async def on_message(message):
    sheetwords = ["sheet link", "link to sheet", "link to the sheet", "payday", "payday friday"]
    if any(word in message.content for word in sheetwords):
        bot_channel = client.get_channel(830820065876115539)
        await bot_channel.send('With this sheet, you can find how many points you have and how much you might get paid this week: http://tinyurl.com/TCHRteam')
    await client.process_commands(message)


## Returns link to the linktr.ee
@client.command(name='links', aliases=['linktree', 'resources'])
async def links(context):
    myEmbed = discord.Embed(title='TCHR Linktr.ee', description='Our linktr.ee is always updated with comp.s and resources that you may find helpful!', color=0x99eecc)
    myEmbed.add_field(name="Linktr.ee",value="https://linktr.ee/tchrnt",inline=False)
    myEmbed.set_footer(text='Created by @michymichelle')
    await context.message.channel.send(embed=myEmbed)


## Help commands
@client.command(pass_context = True)
async def tchrhelp(context):
    embed = discord.Embed(
        title="Help commands",
        description="Below is a list of commands that are currently available on this bot. Prefix is **.**",
        color=0xf1c40f)
    embed.add_field(name=".ping", value="Returns ping latency", inline=False)
    embed.add_field(
        name=".paycheck",
        value="Calculates paycheck for Payday Friday. Enter number of points after command. \nExample: *.paycheck 28000*. \n Aliases: .check, .pcheck, .pay, .paycalculator",
        inline=False)
    embed.add_field(
        name=".top",
        value="Returns specified number of current top racers on the leaderboard. \nExample: *.top 5*, *.top 10*, *.top 20*. \n Aliases: .current, .topnow, .t",
        inline=False)
    embed.add_field(
        name=".crowns",
        value="Returns the winning top 10 racers on the previous week's leaderboard. \nAliases: .top10weekly, t10wk,toptenweek,top10week",
        inline=False)
    embed.add_field(
        name=".sheet",
        value=" Returns spreadsheet link via direct command anywhere in server \nAliases: .link, .sheetlink, .spreadsheet",
        inline=False)
    embed.add_field(
        name="Spreadsheet-related words",
        value="Returns spreadsheet link via mention of keywords in specific channel \nKeywords: sheet link, link to sheet, link to the sheet, payday, payday friday",
        inline=False)
    embed.add_field(
        name=".links",
        value="Returns link to TCHR linktr.ee, where team comps and resources are posted and updated",
        inline=False)
    await context.message.channel.send(embed=embed)


## Discord Client Token
client.run('ODQ0MjIzNjUzMTY3NDk3MjM3.YKPSiw.AuldDR-bNIvMy6jag1U_N6L4uOY')
