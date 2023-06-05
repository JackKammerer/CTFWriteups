import discord
from discord.ext import commands
import io
import logging
import openai
import os
import re
import urllib.request

# Save history log
logging.basicConfig(filename='history.log', encoding='utf-8', format='%(message)s', level=logging.INFO)
# Also log to stderr
logging.getLogger().addHandler(logging.StreamHandler())

openai.api_key = os.environ["OPENAI_API_KEY"]
bot_token = os.environ["DISCORD_BOT_TOKEN"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name="relevantxkcd")
async def relevantxkcd(ctx):
    channel = ctx.channel
    messages = []
    async for message in channel.history(limit=2):
        messages.append(message)
    previous_message = messages[1].content

    async with ctx.typing():
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "You are RelevantXKCD bot. Your sole purpose is to provide links to xkcd comics relevant to the message given to you by the user, based on how well it matches with the information provided on the ExplainXKCD website. You must always respond with a link to an xkcd comic. When you don't know of a link to an xkcd comic relevant to the message, you must instead respond with the link 'https://xkcd.com/{number}' where {number} is a randomly chosen number between 1 and 2781. Your response is always just a single link, no explanation or justification, just one link per message that you send."},
                {"role": "user", "content": "Lol whenever I see the 'permission denied' message I always just throw sudo in front of it without thinking about it"},
                {"role": "assistant", "content": "https://xkcd.com/149"},
                {"role": "user", "content": "agaiheroaerjaeiogahoierhg;eigahi"},
                {"role": "assistant", "content": "https://xkcd.com/213"},
                {"role": "user", "content": previous_message}
            ],
            max_tokens=200,
        )

        result = response['choices'][0]['message']['content'].strip()
        logging.info(f'\n{ctx.message.author.name}: {previous_message}')
        logging.info(f'RelevantXKCD: {result}')
        # Find link in result
        try:
            xkcd_link = re.search(r'https?:\/\/[^\s"\']+', result).group(0)
        except:
            await ctx.send(result)
            return
        if result != xkcd_link:
            await ctx.send(result)

        with urllib.request.urlopen(xkcd_link) as response:
            contents = response.read()
            img_url = re.search(r'Image URL \(for hotlinking\/embedding\):.*?href=.*?"(.*?)"', contents.decode()).group(1)
            filename = img_url.split('/')[-1]
            logging.info(f'Downloading file: {img_url}')
            with urllib.request.urlopen(img_url) as image:
                await ctx.send(file=discord.File(io.BytesIO(image.read()), filename))

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

bot.run(bot_token)

