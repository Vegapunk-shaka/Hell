import asyncio
import re

from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message

from . import HelpMenu, custom_handler, db, handler, hellbot, on_message, Config


@on_message("f", allow_stan=True)
async def set_filter(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, f"Reply to a message with {handler}filter <keyword> to save it as a filter."
        )

    keyword = await hellbot.input(message)
    hell = await hellbot.edit(message, f"Saving filter `{keyword}`")
    msg = await message.reply_to_message.forward(Config.LOGGER_ID)

    await db.set_filter(client.me.id, message.chat.id, keyword.lower(), msg.id)
    await hellbot.delete(hell, f"**🍀 New Filter Saved:** `{keyword}`")
    await msg.reply_text(
        f"**🍀 New Filter Saved:** `{keyword}`\n\n**DO NOT DELETE THIS MESSAGE!!!**",
    )


@on_message(["rmf", "rmaf"], allow_stan=True)
async def rmfilter(client: Client, message: Message):
    if len(message.command[0]) < 9:
        if len(message.command) < 2:
            return await hellbot.delete(message, "Give a filter name to remove.")

        keyword = await hellbot.input(message)
        hell = await hellbot.edit(message, f"Removing filter `{keyword}`")

        if await db.is_filter(client.me.id, message.chat.id, keyword.lower()):
            await db.rm_filter(client.me.id, message.chat.id, keyword.lower())
            await hellbot.delete(hell, f"**🍀 Filter Removed:** `{keyword}`")
        else:
            await hellbot.delete(hell, f"**🍀 Filter does not exists:** `{keyword}`")
    else:
        hell = await hellbot.edit(message, "Removing all filters...")

        await db.rm_all_filters(client.me.id, message.chat.id)
        await hellbot.delete(hell, "All filters have been removed.")


@on_message(["gf", "gaf"], allow_stan=True)
async def allfilters(client: Client, message: Message):
    if len(message.command) > 1:
        keyword = await hellbot.input(message)
        hell = await hellbot.edit(message, f"Getting filter `{keyword}`")

        if await db.is_filter(client.me.id, message.chat.id, keyword.lower()):
            data = await db.get_filter(client.me.id, message.chat.id, keyword.lower())
            msgid = data["filter"][0]["msgid"]
            sent = await client.copy_message(message.chat.id, Config.LOGGER_ID, msgid)

            await sent.reply_text(f"**🍀 Filter:** `{keyword}`")
            await hell.delete()

        else:
            await hellbot.delete(hell, f"**🍀 Filter does not exists:** `{keyword}`")

    else:
        hell = await hellbot.edit(message, "Getting all filters...")
        filters = await db.get_all_filters(client.me.id, message.chat.id)

        if filters:
            text = f"**🍀 No. of Filters in this chat:** `{len(filters)}`\n\n"

            for i, filter in enumerate(filters, 1):
                text += f"** {'0' if i < 10 else ''}{i}:** `{filter['keyword']}`\n"

            await hell.edit(text)

        else:
            await hellbot.delete(hell, "No filters in this chat.")


@custom_handler(filters.incoming & ~filters.service)
async def handle_filters(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
    data = await db.get_all_filters(client.me.id, message.chat.id)
    if not data:
        return

    msg = message.text or message.caption
    if not msg:
        return

    for filter in data:
        pattern = r"( |^|[^\w])" + re.escape(filter["keyword"]) + r"( |$|[^\w])"
        if re.search(pattern, msg, flags=re.IGNORECASE):
            msgid = filter["msgid"]
            await client.copy_message(message.chat.id, Config.LOGGER_ID, msgid)
            await asyncio.sleep(3)


HelpMenu("filters").add(
    "f",
    "<keyword> <reply to a message>",
    "Saves the replied message as a filter to given keyword along the command.",
    "filter hellbot",
    "You need to reply to the message you want to save as filter. You can also save media as filters alonng with captions.",
).add(
    "rmf",
    "<keyword>",
    "Removes the filter with given keyword.",
    "rmfilter hellbot",
).add(
    "rmaf",
    None,
    "Removes all the filters in current chat.",
    "rmallfilter",
).add(
    "gf",
    "<keyword>",
    "Gives the filter data associated with given keyword.",
    "getfilter hellbot",
).add(
    "gaf", None, "Gets all filters in the chat.", "getfilters"
).info(
    "Filter Module"
).done()
