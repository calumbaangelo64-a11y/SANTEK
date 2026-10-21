import discord
from discord import app_commands
import asyncio
import os

# ANG TOKEN KAY KWAON NATO SA RENDER ENVIRONMENT VARIABLES
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

active_spams = {}

@client.event
async def on_ready():
    await tree.sync()
    print(f"[M] Bot Online: {client.user}")

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="start", description="Start auto-spamming")
async def start_spam(interaction: discord.Interaction, message: str):
    channel_id = interaction.channel_id
    
    if channel_id in active_spams:
        return await interaction.response.send_message("Naa nay nagdagan. Type /stop.", ephemeral=True)

    await interaction.response.defer(ephemeral=True)
    
    target_channel = interaction.channel

    await interaction.followup.send("Auto-spam started. Type /stop to end.", ephemeral=True)
    
    async def spam_loop():
        while True:
            try:
                await target_channel.send(message)
            except discord.HTTPException:
                pass
            except Exception as e:
                print(f"[M] Loop Error: {e}")
                break
            await asyncio.sleep(1.0)

    active_spams[channel_id] = asyncio.create_task(spam_loop())

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="stop", description="Stop auto-spamming")
async def stop_spam(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    
    if channel_id in active_spams:
        active_spams[channel_id].cancel()
        del active_spams[channel_id]
        await interaction.response.send_message("Spam stopped.", ephemeral=True)
    else:
        await interaction.response.send_message("Wala may nagdagan diri.", ephemeral=True)

client.run(TOKEN)
