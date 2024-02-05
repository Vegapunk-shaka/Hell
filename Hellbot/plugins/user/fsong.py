import os

from pyrogram import Client
from pyrogram.types import Message

from . import Config, HelpMenu, db, hellbot, on_message

@on_message("fs", allow_stan=True)
async def kangSticker(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "__Reply to any user's audio or video message.__.")

    reply_message = await hellbot.get_reply_message()
    if not reply_message.media and not reply_message.document:
        await eod(hellbot, "__Reply to an audio or video file.__")
        return

    # Check if the replied message is an audio or video file
    if reply_message.media and (reply_message.media.document.mime_type.startswith('audio') or reply_message.media.document.mime_type.startswith('video')):
        chat = "@New736058_bot"
    else:
        await eod(hellbot, "__You can only reply to audio or video files.__")
        return

    if reply_message.sender.bot:
        await eod(hellbot, "__Reply to an actual user's message.__")
        return

    MSG = await eor(hellbot, "__Sending the file to the Database__")

    async with hellbot.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await asyncio.sleep(0.8)
            await MSG.edit("**Done**")
            await asyncio.sleep(0.8)
            await MSG.edit("__Searching the song in the server__")
            await asyncio.sleep(0.8)

        try:
            response = await conv.get_response(timeout=10)
        except asyncio.exceptions.TimeoutError:
            logging.error("1st Response timed out")
            DLT = await MSG.edit("1st Response timed out")
            await asyncio.sleep(15)
            await DLT.delete()
            return

        try:
            response2 = await conv.get_response(timeout=10)
        except asyncio.exceptions.TimeoutError:
            logging.error("2nd Response timed out")
            DLT = await MSG.edit("2nd Response timed out")
            await asyncio.sleep(15)
            await DLT.delete()
            return

        try:
            await MSG.edit("__Getting result.......__")
            await asyncio.sleep(4.5)
            response3 = await conv.get_response(timeout=30)
        except asyncio.exceptions.TimeoutError:
            logging.error("3rd Response timed out")
            DLT = await MSG.edit("3rd Response timed out")
            await asyncio.sleep(15)
            await DLT.delete()
            return

        response_text = response2.text.replace("[Find song](http://t.me/New736058_bot)", "")
        dlt = await MSG.edit("__Parsing the result please wait....__")
        await dlt.delete()

        if "The song could not be found. Try again.​" in response2.text:
            msg_dlt = await hellbot.client.send_message(hellbot.chat_id, response2.text.strip(), reply_to=reply_message)
            await asyncio.sleep(12)
            await msg_dlt.delete()
        elif response3 and response3.media:
            await hellbot.client.send_file(hellbot.chat_id, response3.media, caption=response_text.strip(, reply_to=reply_message)
        else:
            await hellbot.client.send_message(hellbot.chat_id, response_text.strip(), reply_to=reply_message)



HelpMenu("fsong").add(
    "fs",
    " ",
    "Fetches the Song name of the replied audio or video",
    "fsong song finder",
    "Find all song",
).info("Find Song Module").done()
