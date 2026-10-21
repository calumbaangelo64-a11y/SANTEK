import discord
from discord import app_commands
import asyncio
import os

# ANG TOKEN KAY KWAON NATO SA RENDER ENVIRONMENT VARIABLES
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"[M] Bot Online: {client.user}")

# ANG /SPAM COMMAND NGA NAAY AMOUNT
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="spam", description="Spam a message")
async def spam(interaction: discord.Interaction, message: str, amount: int):
    if amount < 1 or amount > 50:
        return await interaction.response.send_message("Max 50 messages.", ephemeral=True)
        
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(f"Spamming {amount} times...", ephemeral=True)
    
    for _ in range(amount):
        try:
            await interaction.channel.send(message)
        except discord.HTTPException:
            pass
        await asyncio.sleep(1.0) # 1 second delay para dili ma-ban sa Discord

client.run(TOKEN)
