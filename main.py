import discord
from discord import app_commands
import asyncio
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = os.getenv("TOKEN")

# DUMMY WEB SERVER PARA DILI MA-TIMEOUT SA RENDER
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()
# -----------------------------------------------------

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"[M] Bot Online: {client.user}")

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
        await asyncio.sleep(1.0)

client.run(TOKEN)
