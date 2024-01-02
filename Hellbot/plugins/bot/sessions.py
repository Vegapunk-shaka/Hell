from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
)

from ..btnsG import gen_inline_keyboard, start_button
from ..btnsK import session_keyboard
from . import START_MSG, BotHelp, Config, Symbols, db, hellbot


@hellbot.bot.on_message(
    filters.command("session") & Config.AUTH_USERS & filters.private
)
async def session_menu(_, message: Message):
    await message.reply_text(
        "**🍀 Please choose an option from below:**",
        reply_markup=session_keyboard(),
    )


@hellbot.bot.on_message(filters.regex(r"New 💫") & Config.AUTH_USERS & filters.private)
async def new_session(_, message: Message):
    await message.reply_text(
        "**Okay!** Let's setup a new session",
        reply_markup=ReplyKeyboardRemove(),
    )

    phone_number = await hellbot.bot.ask(
        message.chat.id,
        "**1.** Enter your telegram account phone number to add the session: \n\n__Send /cancel to cancel the operation.__",
        filters=filters.text,
        timeout=120,
    )

    if phone_number.text == "/cancel":
        return await message.reply_text("**Cancelled!**")
    elif not phone_number.text.startswith("+") and not phone_number.text[1:].isdigit():
        return await message.reply_text(
            "**Error!** Phone number must be in digits and should contain country code."
        )

    try:
        client = Client(
            name="Hellbot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            in_memory=True,
        )
        await client.connect()

        code = await client.send_code(phone_number.text)
        ask_otp = await hellbot.bot.ask(
            message.chat.id,
            "**2.** Enter the OTP sent to your telegram account by separating every number with a space. \n\n**Example:** `2 4 1 7 4`\n\n__Send /cancel to cancel the operation.__",
            filters=filters.text,
            timeout=300,
        )
        if ask_otp.text == "/cancel":
            return await message.reply_text("**Cancelled!**")
        otp = ask_otp.text.replace(" ", "")

        try:
            await client.sign_in(phone_number.text, code.phone_code_hash, otp)
        except SessionPasswordNeeded:
            two_step_pass = await hellbot.bot.ask(
                message.chat.id,
                "**3.** Enter your two step verification password: \n\n__Send /cancel to cancel the operation.__",
                filters=filters.text,
                timeout=120,
            )
            if two_step_pass.text == "/cancel":
                return await message.reply_text("**Cancelled!**")
            await client.check_password(two_step_pass.text)

        session_string = await client.export_session_string()
        await message.reply_text(
            f"**Success!** Your session string is generated. Adding it to database..."
        )
        user_id = (await client.get_me()).id
        await db.update_session(user_id, session_string)
        await client.disconnect()
        await message.reply_text(
            "**Success!** Session string added to database. You can now use HellBot on this account after restarting the bot.\n\n**NOTE:** For security purposes nobody will have the access to your session string. Not even you or the bot."
        )
    except TimeoutError:
        await message.reply_text(
            "**TimeoutError!** You took longer than excpected to complete the process. Please try again."
        )
    except Exception as e:
        await message.reply_text(f"**Error!** {e}")


@hellbot.bot.on_message(
    filters.regex(r"Delete ❌") & Config.AUTH_USERS & filters.private
)
async def delete_session(_, message: Message):
    all_sessions = await db.get_all_sessions()
    if not all_sessions:
        return await message.reply_text("No sessions found in database.")

    collection = []
    for i in all_sessions:
        collection.append((i["user_id"], f"rm_session:{i['user_id']}"))

    buttons = gen_inline_keyboard(collection, 2)
    buttons.append([InlineKeyboardButton("Cancel ❌", "auth_close")])

    await message.reply_text(
        "**Choose a session to delete:**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@hellbot.bot.on_callback_query(filters.regex(r"rm_session"))
async def rm_session_cb(client: Client, cb: CallbackQuery):
    collection = []
    user_id = int(cb.data.split(":")[1])
    all_sessions = await db.get_all_sessions()

    if not all_sessions:
        return await cb.message.delete()

    try:
        owner = await client.get_users(Config.OWNER_ID)
        owner_id = owner.id
        owner_name = owner.first_name
    except:
        owner_id = Config.OWNER_ID
        owner_name = "Owner"
    if cb.from_user.id not in [user_id, owner_id]:
        return await cb.answer(
            f"Access restricted to another users. Only {owner_name} and session client can delete this session!",
            show_alert=True,
        )

    await db.rm_session(user_id)
    await cb.answer("**Success!** Session deleted from database. \n__Restart the bot to apply changes.__", show_alert=True)

    for i in all_sessions:
        collection.append((i["user_id"], f"rm_session:{i['user_id']}"))

    buttons = gen_inline_keyboard(collection, 2)
    buttons.append([InlineKeyboardButton("Cancel ❌", "auth_close")])

    await cb.message.edit_reply_markup(InlineKeyboardMarkup(buttons))


@hellbot.bot.on_message(filters.regex(r"List 📜") & Config.AUTH_USERS & filters.private)
async def list_sessions(_, message: Message):
    all_sessions = await db.get_all_sessions()
    if not all_sessions:
        return await message.reply_text("No sessions found in database.")

    text = f"**{Symbols.cross_mark} List of sessions:**\n\n"
    for i, session in enumerate(all_sessions):
        text += f"[{'0' if i <= 9 else ''}{i+1}] {Symbols.bullet} **User ID:** `{session['user_id']}`\n"

    await message.reply_text(text)


@hellbot.bot.on_message(filters.regex(r"Home 🏠") & filters.private & Config.AUTH_USERS)
async def go_home(_, message: Message):
    await message.reply_text(
        "**Home 🏠**",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.reply_text(
        START_MSG.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(start_button()),
    )


BotHelp("Sessions").add(
    "session", "This command is packed with tools to manage userbot sessions."
).info(
    "Session 🚀"
).done()
