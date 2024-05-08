from pyrogram import Client, filters
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
    with open(file_path, "rb") as fp:
        content = fp.read()
        image_md5 = base64.b64encode(hashlib.md5(content).digest()).decode("utf-8")
    return image_md5, content

@user.on_message(filters.command(["ups"]))
async def enhance_command(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo[-1]
        file_path = f"{photo.file_id}.jpg"
        await photo.download(file_path)
        await message.reply("<b>Enhancing your photo...</b>")
        
        image_md5, content = _get_image_md5_content(file_path)

        async with httpx.AsyncClient(
            base_url=_BASE_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
        ) as client:
            response = await client.post(
                "/tasks",
                json={
                    "tools": [
                        {"type": "face_enhance", "mode": "beautify"},
                        {"type": "background_enhance", "mode": "base"}
                    ],
                    "image_md5": image_md5,
                    "image_content_type": CONTENT_TYPE
                }
            )
            assert response.status_code == 200
            body = response.json()
            task_id = body["task_id"]

            response = await client.put(
                body["upload_url"],
                headers=body["upload_headers"],
                content=content,
                timeout=_TIMEOUT
            )
            assert response.status_code == 200

            response = await client.post(f"/tasks/{task_id}/process")
            assert response.status_code == 202

            for i in range(50):
                response = await client.get(f"/tasks/{task_id}")
                assert response.status_code == 200

                if response.json()["status"] == "completed":
                    break
                else:
                    await asyncio.sleep(2)

            output_url = response.json()["result"]["output_url"]
            await user.send_message(message.chat.id, f"<b>Enhanced photo: </b> {output_url}")

        os.remove(file_path)
    else:
        await message.reply("<b>Please reply to a photo to enhance it.</b>")
