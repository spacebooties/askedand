import os
import discord

from discord import app_commands
from dotenv import load_dotenv

from core.sources import run as sources_run
from core.debate import run as debate_run
from core.question import run as question_run

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN missing from .env")

intents = discord.Intents.default()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(
    name="sources",
    description="Show sources and claims"
)
async def sources(
    interaction: discord.Interaction,
    question: str
):

    await interaction.response.defer(thinking=True)

    try:
        result = sources_run(question)

        if len(result) > 1900:
            result = result[:1900]

        await interaction.followup.send(result)

    except Exception as e:
        await interaction.followup.send(
            f"Error: {str(e)}"
        )


@tree.command(
    name="debate",
    description="Show two sides of an issue"
)
async def debate(
    interaction: discord.Interaction,
    question: str
):

    await interaction.response.defer(thinking=True)

    try:
        result = debate_run(question)

        if len(result) > 1900:
            result = result[:1900]

        await interaction.followup.send(result)

    except Exception as e:
        await interaction.followup.send(
            f"Error: {str(e)}"
        )


@tree.command(
    name="question",
    description="Generate a thought-provoking question"
)
async def question(
    interaction: discord.Interaction,
    topic: str
):

    await interaction.response.defer(thinking=True)

    try:
        result = question_run(topic)

        await interaction.followup.send(result)

    except Exception as e:
        await interaction.followup.send(
            f"Error: {str(e)}"
        )


@client.event
async def on_ready():

    await tree.sync()

    print()
    print("====================")
    print(f"Logged in as {client.user}")
    print("Slash commands synced.")
    print("====================")
    print()


client.run(TOKEN)