from pyrogram import Client, filters
from PIL import Image
import requests
from io import BytesIO
from . import HelpMenu, hellbot, on_message

@on_message("ups", allow_stan=True)
def upscale_image(client, message):
    chat_id = message.chat.id
    file_id = message.photo.file_id

    file = client.get_photo(file_id)
    image_url = file.file_path

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    image = image.resize((image.size[0]*2, image.size[1]*2))

    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0)

    client.send_photo(chat_id, photo=output)

app.run()
