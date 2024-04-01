from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from Hellbot.functions.templates import command_template, help_template

from ..btnsG import gen_bot_help_buttons, gen_inline_help_buttons, start_button
from . import HELP_MSG, START_MSG, Config, Symbols, hellbot


async def check_auth_click(cb: CallbackQuery) -> bool:
    if cb.from_user.id not in Config.AUTH_USERS:
        await cb.answer(
            "You are not authorized to use this bot. \n\n</> @Chowdhury_Siam",
            show_alert=True,
        )
        return False
    return True


@hellbot.bot.on_callback_query(filters.regex(r"auth_close"))
async def auth_close_cb(_, cb: CallbackQuery):
    if await check_auth_click(cb):
        await cb.message.delete()


@hellbot.bot.on_callback_query(filters.regex(r"close"))
async def close_cb(_, cb: CallbackQuery):
    await cb.message.delete()


@hellbot.bot.on_callback_query(filters.regex(r"bot_help_menu"))
async def bot_help_menu_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    plugin = str(cb.data.split(":")[1])

    try:
        buttons = [
            InlineKeyboardButton(f"{Symbols.bullet} {i}", f"bot_help_cmd:{plugin}:{i}")
            for i in sorted(Config.BOT_HELP[plugin]["commands"])
        ]
    except KeyError:
        await cb.answer("No description provided for this plugin!", show_alert=True)
        return

    buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    buttons.append([InlineKeyboardButton(Symbols.back, "help_data:bothelp")])

    caption = (
        f"**Plugin File:** `{plugin}`\n"
        f"**Plugin Info:** __{Config.BOT_HELP[plugin]['info']} 🍀__\n\n"
        f"**📃 Loaded Commands:** `{len(sorted(Config.BOT_HELP[plugin]['commands']))}`"
    )

    try:
        await cb.edit_message_text(
            caption,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception:
        # handles MessageNotModified error
        pass


@hellbot.bot.on_callback_query(filters.regex(r"bot_help_cmd"))
async def bot_help_cmd_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    result = ""
    plugin = str(cb.data.split(":")[1])
    command = str(cb.data.split(":")[2])
    cmd_dict = Config.BOT_HELP[plugin]["commands"][command]

    result += f"**{Symbols.radio_select} Command:** `/{cmd_dict['command']}`"
    result += (
        f"\n\n**{Symbols.arrow_right} Description:** __{cmd_dict['description']}__"
    )
    result += f"\n\n**<\\> @Chowdhury_Siam 🍀**"

    buttons = [
        [
            InlineKeyboardButton(Symbols.back, f"bot_help_menu:{plugin}"),
            InlineKeyboardButton(Symbols.close, "help_data:botclose"),
        ]
    ]

    try:
        await cb.edit_message_text(
            result,
            ParseMode.MARKDOWN,
            True,
            InlineKeyboardMarkup(buttons),
        )
    except Exception:
        # handles MessageNotModified error
        pass


@hellbot.bot.on_callback_query(filters.regex(r"help_page"))
async def help_page_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    page = int(cb.data.split(":")[1])
    buttons, max_page = await gen_inline_help_buttons(page, sorted(Config.CMD_MENU))

    caption = await help_template(
        cb.from_user.mention,
        (len(Config.CMD_INFO), len(Config.CMD_MENU)),
        (page + 1, max_page),
    )

    try:
        await cb.edit_message_text(
            caption,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception:
        # handles MessageNotModified error
        pass


@hellbot.bot.on_callback_query(filters.regex(r"help_menu"))
async def help_menu_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    page = int(cb.data.split(":")[1])
    plugin = str(cb.data.split(":")[2])

    try:
        buttons = [
            InlineKeyboardButton(
                f"{Symbols.bullet} {i}", f"help_cmd:{page}:{plugin}:{i}"
            )
            for i in sorted(Config.HELP_DICT[plugin]["commands"])
        ]
    except KeyError:
        await cb.answer("No description provided for this plugin!", show_alert=True)
        return

    buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    buttons.append([InlineKeyboardButton(Symbols.back, f"help_page:{page}")])

    caption = await command_template(
        plugin,
        Config.HELP_DICT[plugin]["info"],
        len(sorted(Config.HELP_DICT[plugin]["commands"])),
    )

    try:
        await cb.edit_message_text(
            caption,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception:
        # handles MessageNotModified error
        pass


@hellbot.bot.on_callback_query(filters.regex(r"help_cmd"))
async def help_cmd_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    page = int(cb.data.split(":")[1])
    plugin = str(cb.data.split(":")[2])
    command = str(cb.data.split(":")[3])
    result = ""
    cmd_dict = Config.HELP_DICT[plugin]["commands"][command]

    if cmd_dict["parameters"] is None:
        result += f"**{Symbols.radio_select} Command:** `{Config.HANDLERS[0]}{cmd_dict['command']}`"
    else:
        result += f"**{Symbols.radio_select} Command:** `{Config.HANDLERS[0]}{cmd_dict['command']} {cmd_dict['parameters']}`"

    if cmd_dict["description"]:
        result += (
            f"\n\n**{Symbols.arrow_right} Description:** __{cmd_dict['description']}__"
        )

    if cmd_dict["example"]:
        result += f"\n\n**{Symbols.arrow_right} Example:** `{Config.HANDLERS[0]}{cmd_dict['example']}`"

    if cmd_dict["note"]:
        result += f"\n\n**{Symbols.arrow_right} Note:** __{cmd_dict['note']}__"

    result += f"\n\n**<\\> @Chowdhury_Siam 🍀**"

    buttons = [
        [
            InlineKeyboardButton(Symbols.back, f"help_menu:{page}:{plugin}"),
            InlineKeyboardButton(Symbols.close, "help_data:c"),
        ]
    ]

    try:
        await cb.edit_message_text(
            result,
            ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception:
        # handles MessageNotModified error
        pass


@hellbot.bot.on_callback_query(filters.regex(r"help_data"))
async def help_close_cb(_, cb: CallbackQuery):
    if not await check_auth_click(cb):
        return

    action = str(cb.data.split(":")[1])
    if action == "c":
        await cb.edit_message_text(
            "**Help Menu Closed!**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Reopen", "help_data:reopen")]]
            ),
        )
    elif action == "reopen":
        buttons, pages = await gen_inline_help_buttons(0, sorted(Config.CMD_MENU))
        caption = await help_template(
            cb.from_user.mention,
            (len(Config.CMD_INFO), len(Config.CMD_MENU)),
            (1, pages),
        )
        await cb.edit_message_text(
            caption,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif action == "botclose":
        await cb.message.delete()
    elif action == "bothelp":
        buttons = await gen_bot_help_buttons()
        await cb.edit_message_text(
            HELP_MSG,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif action == "source":
        buttons = [
            [
                InlineKeyboardButton("🚀 Deploy", url="https://t.me/Chowdhury_Siam"),
                InlineKeyboardButton("Plugins 📂", url="https://t.me/Chowdhury_Siam"),
            ],
            [
                InlineKeyboardButton("Anime Kun", url="https://t.me/Anime_Kun_Channel"),
            ],
            [
                InlineKeyboardButton("🎙️ Support", url="https://t.me/Chowdhury_Siam"),
                InlineKeyboardButton("Updates 📣", url="https://t.me/AnimeKunChannel"),
            ],
            [
                InlineKeyboardButton("🔙", "help_data:start"),
                InlineKeyboardButton(Symbols.close, "help_data:botclose"),
            ],
        ]
        await cb.edit_message_text(
            "__» The source code is available on GitHub. You can find the link below.__\n"
            "__» Every project available under The-RinBot are open-source and free to use and modify to your needs.__\n"
            "__» Anyone pretending to be the developer of this bot and selling the code, is a scammer.__\n\n"
            "__» Please consider giving a star to the repository if you liked the project.__\n"
            "__» Feel free to contact us if you need any help regarding the source code.__\n\n"
            "**❤️ @Chowdhury_Siam**",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif action == "start":
        buttons = start_button()
        await cb.edit_message_text(
            START_MSG.format(cb.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
)
                           
