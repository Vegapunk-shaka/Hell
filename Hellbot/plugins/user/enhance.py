from pyrogram import Client, filters
from . import HelpMenu, hellbot, on_message
import os
from pyrogram.types import Message
import requests

api_key = "VqhGPCcCL59BaNicWsgxTXH-kmwuVBMSdz0poqEZZXqgfr5Y"

@Client.on_message("ups", allow_stan=True)
async def enhance_photo(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo
        file_path = await client.download_media(photo.file_id)
        
        url = f"https://removal.ai/api/remote/v1/enhance?api_key={api_key}"
        
        try:
            async with client.http.post(url, files={"file": open(file_path, "rb")}) as response:
                if response.status_code == 200:
                    enhanced_image = await response.read()
                    # Convert the enhanced image to a file-like object for sending
                    enhanced_image_file = io.BytesIO(enhanced_image)
                    await client.send_photo(message.chat.id, enhanced_image_file, caption="Enhanced image")
                else:
                    await message.reply_text("Failed to enhance the photo")
        except Exception as e:
            await message.reply_text(f"An error occurred: {e}")
        finally:
            os.remove(file_path)
    else:
        await message.reply_text("Please reply to a photo to enhance it.")
