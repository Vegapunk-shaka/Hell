from pyrogram import Client, filters
from PIL import Image
import requests
from io import BytesIO
import os

API_ID = 28986163  # Your API ID
API_HASH = "07225d0de9bee70666517315d2174171"  # Your API Hash

# Initialize the Pyrogram Client
app = Client("my_image_upscale_bot", api_id=API_ID, api_hash=API_HASH)

# Function to upscale the image
async def upscale_image(client, message):
    chat_id = message.chat.id
    
    if message.photo is None:
        await client.send_message(chat_id, "Please send an image to upscale.")
        return
    
    file_id = message.photo.file_id

    file = await client.get_photo(file_id)
    image_url = file.file_path

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    image = image.resize((image.size[0]*2, image.size[1]*2))

    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0)

    await client.send_photo(chat_id, photo=output)

# Registering the upscale_image function as a message handler
@app.on_message(filters.command("upscale", prefixes="/"))
async def upscale_command(client, message):
    await upscale_image(client, message)

# Start the bot
if __name__ == '__main__':
    app.run()
