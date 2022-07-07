import os
import openai
import discord

openai.api_key = os.getenv("OPENAI_API_KEY")
discord_bot = os.getenv("DISCORD_BOT_KEY")

client = discord.Client()

generation_commands = {
    '.greentext': "Write a 4chan greentext about",
    '.aita': "Write a reddit AITA post about",
}


def generate_text(prompt: str) -> str:
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

    if message.content == ".help":
        out = "```\n"
        for k, v in generation_commands.items():
            out += f"{k} - {v}\n"
        out += "```"
        await message.reply(out)

    for k, v in generation_commands.items():
        if message.content.startswith(k):
            subject = f'"{message.content[len(k)+1:]}"'
            await message.reply(f"```\n{generate_text(f'{v} {subject}')}\n```")


@client.event
async def on_ready():
    print('------------')
    print(f'Logged in as "{client.user.name}"')
    print('id: ', client.user.id)
    print('------------')

client.run(discord_bot)
