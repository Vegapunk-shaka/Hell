import os
import time

import requests
from pyrogram.types import Message
from yt_dlp import YoutubeDL

from Hellbot.functions.driver import YoutubeDriver
from Hellbot.functions.formatter import secs_to_mins
from Hellbot.functions.tools import progress

from . import HelpMenu, Symbols, hellbot, on_message


@on_message("yta", allow_stan=True)
async def youtube_audio(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(
            message, "Give a valid youtube link to download audio."
        )

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Checking ...")
    status, url = YoutubeDriver.check_url(query)

    if not status:
        return await hellbot.delete(hell, url)

    await hell.edit("🎼 __Downloading audio ...__")
    try:
        with YoutubeDL(YoutubeDriver.song_options()) as ytdl:
            yt_data = ytdl.extract_info(url, False)
            yt_file = ytdl.prepare_filename(yt_data)
            ytdl.process_info(yt_data)

        upload_text = f"**⬆️ Uploading Song ...** \n\n**{Symbols.anchor} Title:** `{yt_data['title'][:50]}`\n**{Symbols.anchor} Channel:** `{yt_data['channel']}`"
        await hell.edit(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)

        await message.reply_audio(
            f"{yt_file}.mp3",
            caption=f"**🎧 Title:** {yt_data['title']} \n\n**👀 Views:** `{yt_data['view_count']}` \n**⌛ Duration:** `{secs_to_mins(int(yt_data['duration']))}`",
            duration=int(yt_data["duration"]),
            performer="[Sɪᴀᴍ Cʜᴏᴡᴅʜᴜʀʏ]",
            title=yt_data["title"],
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                hell,
                time.time(),
                upload_text,
            ),
        )
        await hell.delete()
    except Exception as e:
        return await hellbot.delete(hell, f"**🍀 Audio not Downloaded:** `{e}`")

    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp3")
    except:
        pass


@on_message("ytv", allow_stan=True)
async def ytvideo(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(
            message, "Give a valid youtube link to download video."
        )

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Checking ...")
    status, url = YoutubeDriver.check_url(query)

    if not status:
        return await hellbot.delete(hell, url)

    await hell.edit("🎼 __Downloading video ...__")
    try:
        with YoutubeDL(YoutubeDriver.video_options()) as ytdl:
            yt_data = ytdl.extract_info(url, True)
            yt_file = yt_data["id"]

        upload_text = f"**⬆️ Uploading Song ...** \n\n**{Symbols.anchor} Title:** `{yt_data['title'][:50]}`\n**{Symbols.anchor} Channel:** `{yt_data['channel']}`"
        await hell.edit(upload_text)
        response = requests.get(f"https://i.ytimg.com/vi/{yt_data['id']}/hqdefault.jpg")
        with open(f"{yt_file}.jpg", "wb") as f:
            f.write(response.content)

        await message.reply_video(
            f"{yt_file}.mp4",
            caption=f"**🎧 Title:** {yt_data['title']} \n\n**👀 Views:** `{yt_data['view_count']}` \n**⌛ Duration:** `{secs_to_mins(int(yt_data['duration']))}`",
            duration=int(yt_data["duration"]),
            thumb=f"{yt_file}.jpg",
            progress=progress,
            progress_args=(
                hell,
                time.time(),
                upload_text,
            ),
        )
        await hell.delete()
    except Exception as e:
        return await hellbot.delete(hell, f"**🍀 Video not Downloaded:** `{e}`")

    try:
        os.remove(f"{yt_file}.jpg")
        os.remove(f"{yt_file}.mp4")
    except:
        pass


@on_message("ytlink", allow_stan=True)
async def ytlink(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give something to search on youtube.")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Searching ...")

    try:
        results = YoutubeDriver(query, 7).to_dict()
    except Exception as e:
        return await hellbot.delete(hell, f"**🍀 Error:** `{e}`")

    if not results:
        return await hellbot.delete(hell, "No results found.")

    text = f"**🔎 Total Results Found:** `{len(results)}`\n\n"
    for result in results:
        text += f"    **{Symbols.anchor} Title:** `{result['title'][:50]}`\n**{Symbols.anchor} Channel:** `{result['channel']}`\n**{Symbols.anchor} Views:** `{result['views']}`\n**{Symbols.anchor} Duration:** `{result['duration']}`\n**{Symbols.anchor} Link:** `https://youtube.com{result['url_suffix']}`\n\n"

    await hell.edit(text, disable_web_page_preview=True)


HelpMenu("youtube").add(
    "yta",
    "<youtube link>",
    "Download the youtube video in .mp3 format!",
    "yta https://youtu.be/xxxxxxxxxxx",
).add(
    "ytv",
    "<youtube link>",
    "Download the youtube video in .mp4 format!",
    "ytv https://youtu.be/xxxxxxxxxxx",
).add(
    "ytlink",
    "<query>",
    "Search for a video on youtube.",
    "ytlink the hellbot",
).info(
    "Youtube Downloader",
).done()
