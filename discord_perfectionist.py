import discord
from perfectionist_board import PerfectionistBoard
from fetch_daily_board import fetch_daily_board, fetch_board, fetch_weekly_board

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        if message.content.startswith('!daily'):
            await message.channel.send('Give me a few moments...')
            score = PerfectionistBoard(fetch_daily_board(2)).attempt_solve()
            await message.channel.send('Best score I could find is: ' + str(score))
            f = open("output.html", "rb")
            await message.channel.send(file=discord.File(f))
        elif message.content.startswith('!weekly'):
            await message.channel.send('Give me a while...')
            score = PerfectionistBoard(fetch_weekly_board(2)).attempt_solve()
            await message.channel.send('Best score I could find is: ' + str(score))
            f = open("output.html", "rb")
            await message.channel.send(file=discord.File(f))
        elif message.content.startswith('!version'):
            await message.channel.send('`v1.0.0`')
    except Exception:
        await message.channel.send("There was an error")
        raise Exception


if __name__ == "__main__":
    client.run('NzM0NzU5OTMzNzQ4NDQ1Mjk2.XxWYgw.jlhkf0Kv2WUFpPx0yLsl6XJmrGc')