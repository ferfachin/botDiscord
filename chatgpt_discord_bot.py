import os
import openai
import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv  

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

intents = Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message received: {message.content}")

    if message.content.startswith('!chat'):
        print("Chat command detected")
        await chat(message)

async def chat(message):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{message.content[5:].strip()}",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )
        chat_response = response.choices[0].text.strip()
        await message.channel.send(chat_response)
    except Exception as e:
        print(f"Error: {e}")
        await message.channel.send("Sorry, I couldn't process your request.")

bot.run(TOKEN)
