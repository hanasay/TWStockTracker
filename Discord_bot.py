import twstock
import discord
from discord.ext import commands

with open('Discord_token.txt', 'r') as file
    discord_token=file.readline()

# intents是要求機器人的權限
intents = discord.Intents.all()
# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")

@bot.command()
# 輸入%Hello呼叫指令
async def watch(ctx, stock_ID):
    # 回覆Hello, world!
    stock = twstock.realtime.get([stock_ID])

    stock = stock[stock_ID]

    current_price = stock['realtime']['latest_trade_price']

    return_text = '現價: ' + current_price

    await ctx.send(return_text)

bot.run(discord_token)
#while 1:
#    print(twstock.realtime.get(['2330']))