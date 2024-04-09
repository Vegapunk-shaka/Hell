from telethon import TelegramClient, events
from PIL import Image
import requests
from io import BytesIO
import os

API_ID = 28986163  # Your API ID
API_HASH = "07225d0de9bee70666517315d2174171"  # Your API Hash

client = TelegramClient("my_image_upscale_bot", API_ID, API_HASH)

# Function to upscale the image
async def upscale_image(event):
    chat_id = event.chat_id
    
    if not event.photo:
        await event.respond("Please send an image to upscale.")
        return
    
    image = await event.download_media()
    with Image.open(image) as img:
        img = img.resize((img.size[0]*2, img.size[1]*2))
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        await client.send_file(chat_id, img_bytes)

# Registering the upscale_image function as a message handler
@client.on(events.NewMessage(pattern='.ups'))
async def upscale_command(event):
    await upscale_image(event)

# Start the userbot
if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
