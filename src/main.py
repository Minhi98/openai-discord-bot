import os
import openai
import discord

openai.api_key = os.getenv("OPENAI_API_KEY")
discord_bot = os.getenv("DISCORD_BOT_KEY")

client = discord.Client()


def generate_greentext(prompt: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return os.linesep.join([s for s in response["choices"][0]["text"].splitlines() if s])


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.greentext '):
        subject = '"' + message.content[11:] + '"'
        await message.reply(f"```\n{generate_greentext(f'Write a 4chan greentext about {subject}')}\n```")

    if message.content.startswith('.aita '):
        subject = '"' + message.content[6:] + '"'
        await message.reply(f"```\n{generate_greentext(f'Write a reddit AITA post about {subject}')}\n```")


@client.event
async def on_ready():
    print('------------')
    print(f'Logged in as "{client.user.name}"')
    print('id: ', client.user.id)
    print('------------')

client.run(discord_bot)
