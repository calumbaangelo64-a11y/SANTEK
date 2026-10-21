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
    print(f"[M] Fast Spammer Online: {client.user}")

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="spam", description="Spam a message fast")
async def spam(interaction: discord.Interaction, message: str, amount: int):
    # Max limit is 100
    if amount < 1 or amount > 100:
        return await interaction.response.send_message("Max 100 messages.", ephemeral=True)
        
    await interaction.response.defer(ephemeral=True)
    
    for i in range(amount):
        try:
            # followup.send sends the actual message to the channel
            await interaction.followup.send(message)
        except discord.HTTPException:
            pass # Skip if rate limited so it doesn't crash
        except Exception as e:
            print(f"[M] Error: {e}")
            
        # 0.4 seconds delay. Fast but won't instantly get you banned.
        await asyncio.sleep(0.4) 

client.run(TOKEN)
