from pyrogram import Client, filters
from . import HelpMenu, hellbot, on_message
import os
from pyrogram.types import Message
import requests

api_key = "VqhGPCcCL59BaNicWsgxTXH-kmwuVBMSdz0poqEZZXqgfr5Y"

@on_message("ups", allow_stan=True)
async def enhance_photo(client, message: Message):
    if message.reply_to_message and message.reply_to_message.photo:
        photo_id = message.reply_to_message.photo.file_id
        file_path = await client.download_media(photo_id)
        
        url = "https://removal.ai/api/remote/v1/enhance?api_key={}".format(api_key)
        files = {'file': open(file_path, 'rb')}
        
        response = requests.post(url, files=files)
        enhanced_image = response.content

        await client.send_photo(message.chat.id, enhanced_image, caption="Enhanced image")

        os.remove(file_path)

    else:
        await message.reply_text("Please reply to a photo to enhance it.")
