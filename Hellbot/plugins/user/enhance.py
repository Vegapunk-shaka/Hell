from pyrogram import Client, filters
from . import HelpMenu, hellbot, on_message
import base64
import hashlib
import httpx
import os

API_KEY = "VqhGPCcCL59BaNicWsgxTXH-kmwuVBMSdz0poqEZZXqgfr5Y"
CONTENT_TYPE = "image/jpeg"
_TIMEOUT = 30
_BASE_URL = "https://developer.remini.ai/api"

# Assuming you have an existing Pyrogram Client instance named "user"

def _get_image_md5_content(file_path: str) -> tuple[str, bytes]:
    if os.path.exists(file_path):
        with open(file_path, "rb") as fp:
            content = fp.read()
            image_md5 = base64.b64encode(hashlib.md5(content).digest()).decode("utf-8")
        return image_md5, content
    else:
        print(f"File not found at path: {file_path}")
        return None, None

@on_message("ups", allow_stan=True)
async def enhance_command(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo
        file_path = f"{photo.file_id}.jpg"
        
        # Download the photo
        await client.download_media(photo, file_path)
        
        # Check if the file exists
        if os.path.exists(file_path):
            image_md5, content = _get_image_md5_content(file_path)
            
            if image_md5 and content:
                await message.reply("<b>Enhancing your photo...</b>")
                # Continue with the image enhancement process
            else:
                await message.reply("<b>Error: Unable to process file.</b>")
        else:
            print(f"File not found at path: {file_path}")
            await message.reply("<b>Error: File not found.</b>")
    else:
        await message.reply("<b>Please reply to a photo to enhance it.</b>")
