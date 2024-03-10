import asyncio

from pyrogram import Client
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from Hellbot.core import LOGS

from . import HelpMenu, group_only, handler, hellbot, on_message


@on_message(
    "promote",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def promote(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, "Need a username/id or reply to a user to promote them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        title = await hellbot.input(message)
    else:
        user = await client.get_users(message.command[1])
        title = (await hellbot.input(message)).split(" ", 1)[1].strip() or ""

    try:
        privileges = ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False,
            is_anonymous=False,
        )
        await message.chat.promote_member(user.id, privileges)
        await client.set_administrator_title(message.chat.id, user.id, title)
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(message, f"**💫 Promoted {user.mention} successfully!**")
    await hellbot.check_and_log(
        "promote",
        f"**Promoted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "demote",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def demote(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, "Need a username/id or reply to a user to demote them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])
    try:
        privileges = ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            is_anonymous=False,
        )
        await message.chat.promote_member(user.id, privileges)
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(message, f"**🙄 Demoted {user.mention} successfully!**")
    await hellbot.check_and_log(
        "demote",
        f"**Demoted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "ban",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def ban(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) < 2:
            reason = None
        else:
            reason = await hellbot.input(message)
    elif len(message.command) == 2:
        user = await client.get_users(message.command[1])
        reason = None
    elif len(message.command) > 2:
        user = await client.get_users(message.command[1])
        reason = (await hellbot.input(message)).split(" ", 1)[1].strip()
    else:
        return await hellbot.delete(
            message, "Need a username/id or reply to a user to ban them!"
        )

    try:
        await message.chat.ban_member(user.id)
    except Exception as e:
        return await hellbot.error(message, e)

    reason = reason if reason else "Not Specified"
    await hellbot.delete(
        message,
        f"**☠️ Banned {user.mention} successfully!**\n**Reason:** `{reason}`",
        30,
    )
    await hellbot.check_and_log(
        "ban",
        f"**Banned User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unban",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def unban(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, "Need a username/id or reply to a user to unban them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    try:
        await message.chat.unban_member(user.id)
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(message, f"**🤗 Unbanned {user.mention} Successfully!**", 30)
    await hellbot.check_and_log(
        "unban",
        f"**Unbanned User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "kick",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def kick(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) < 2:
            reason = None
        else:
            reason = await hellbot.input(message)
    elif len(message.command) == 2:
        user = await client.get_users(message.command[1])
        reason = None
    elif len(message.command) > 2:
        user = await client.get_users(message.command[1])
        reason = (await hellbot.input(message)).split(" ", 1)[1].strip()
    else:
        return await hellbot.delete(
            message, "Need a username/id or reply to a user to kick them!"
        )

    try:
        await message.chat.ban_member(user.id)
    except Exception as e:
        return await hellbot.error(message, e)

    reason = reason if reason else "Not Specified"
    await hellbot.delete(
        message,
        f"**👋 Kicked {user.mention} Successfully!**\n**Reason:** `{reason}`",
        30,
    )
    await hellbot.check_and_log(
        "kick",
        f"**Kicked User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )
    await asyncio.sleep(5)
    await message.chat.unban_member(user.id)


@on_message(
    "mute",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def mute(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) < 2:
            reason = None
        else:
            reason = await hellbot.input(message)
    elif len(message.command) == 2:
        user = await client.get_users(message.command[1])
        reason = None
    elif len(message.command) > 2:
        user = await client.get_users(message.command[1])
        reason = (await hellbot.input(message)).split(" ", 1)[1].strip()
    else:
        return await hellbot.delete(
            message, "Need a username/id or reply to a user to mute them!"
        )

    try:
        permissions = ChatPermissions(
            can_send_messages=False,
        )
        await message.chat.restrict_member(user.id, permissions)
    except Exception as e:
        return await hellbot.error(message, e)

    reason = reason if reason else "Not Specified"
    await hellbot.delete(
        message, f"**🤐 Muted {user.mention} Successfully!**\n**Reason:** `{reason}`", 30
    )
    await hellbot.check_and_log(
        "mute",
        f"**Muted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unmute",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def unmute(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, "Need a username/id or reply to a user to unmute them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    try:
        permissions = ChatPermissions(
            can_send_messages=True,
        )
        await message.chat.restrict_member(user.id, permissions)
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(message, f"**😁 Unmuted {user.mention} Successfully!**", 30)
    await hellbot.check_and_log(
        "unmute",
        f"**Unmuted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )

@on_message(
    "dmute",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def startmute(client: Client, message: Message):
    xx = await hellbot.delete(message,f"**Muting...**", 5)
    if input_ := hellbot.pattern_match.group(1).strip():
        try:
            userid = await hellbot.client.parse_id(input_)
        except Exception as x:
            return await xx.edit(str(x))
    elif hellbot.reply_to_msg_id:
        reply = await hellbot.get_reply_message()
        userid = reply.sender_id
        if reply.out or userid in [hellbot.me.id, asst.me.id]:
            return await hellbot.delete(message,f"**You cannot mute yourself or your assistant bot.**", 30)
    elif hellbot.is_private:
        userid = hellbot.chat_id
    else:
        return await hellbot.delete(message,f"**Reply to a user or add their userid.**", 5)
    chat = await hellbot.get_chat()
    if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
        if not chat.admin_rights.delete_messages:
            return await hellbot.delete(message,f"**No proper admin rights...**", 5)
    elif "creator" not in vars(chat) and not hellbot.is_private:
        return await hellbot.delete(message,f"**No proper admin rights...**", 5)
    if is_muted(hellbot.chat_id, userid):
        return await hellbot.delete(message,f"**This user is already muted in this chat.**", 5)
    mute(hellbot.chat_id, userid)
    await hellbot.delete(message,f"**Successfully muted...**", 3)


@on_message(
    "pin",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Need a reply to pin a message!")

    try:
        await message.reply_to_message.pin()
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(
        message,
        f"**📌 Pinned [Message]({message.reply_to_message.link}) in {message.chat.title}!**",
        30,
    )
    await hellbot.check_and_log(
        "pin",
        f"**Pinned Message**\n\n**Message:** [Click Here]({message.reply_to_message.link})\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unpin",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def unpin(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Need a reply to unpin a message!")

    try:
        await message.reply_to_message.unpin()
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(
        message,
        f"**📌 Unpinned [Message]({message.reply_to_message.link}) in {message.chat.title}!**",
        30,
    )
    await hellbot.check_and_log(
        "unpin",
        f"**Unpinned Message**\n\n**Message:** [Click Here]({message.reply_to_message.link})\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "zombies",
    chat_type=group_only,
    admin_only=False,
    allow_stan=False,
)
async def zombies(_, message: Message):
    hell = await hellbot.edit(message, "☠️ Detecting zombies...")
    ded_users = []
    async for members in message.chat.get_members():
        if members.user.is_deleted:
            ded_users.append(members.user.id)

    if not ded_users:
        return await hell.edit(
            "🫡 Don't have any zombies in this group. **Groups' clean AF!**"
        )

    if len(message.command) > 1 and message.command[1].lower() == "clean":
        await hell.edit(
            f"☠️ Found {len(ded_users)} zombies... **🔫 Time to purge them!**"
        )
        failed = 0
        success = 0
        for user in ded_users:
            try:
                await message.chat.ban_member(user)
                success += 1
            except Exception as e:
                LOGS.error(e)
                failed += 1

        await hell.edit(f"**Purged {success} zombies!**\n`{failed}` holds immunity!")
    else:
        await hell.edit(
            f"**☠️ Found {len(ded_users)} zombies!**\n\n__Use__ `{handler}zombies clean` __to kill them!__"
        )


HelpMenu("admin").add(
    "promote", "<username/id/reply> <title>", "Promote a user to admin.", "promote @"
).add(
    "demote", "<username/id/reply>", "Demote a user from admin.", "demote @"
).add(
    "ban", "<username/id/reply> <reason>", "Ban a user from the group.", "ban @"
).add(
    "unban", "<username/id/reply>", "Unban a user from the group.", "unban @"
).add(
    "kick", "<username/id/reply> <reason>", "Kick a user from the group.", "kick @"
).add(
    "mute", "<username/id/reply> <reason>", "Mute a user in the group", "mute @"
).add(
    "unmute", "<username/id/reply>", "Unmute a user in the group.", "unmute @"
).add(
    "pin", "<reply>", "Pin the replied message in the group."
).add(
    "unpin", "<reply>", "Unpin the replied pinned message in the group."
).add(
    "zombies", "clean", "Finds the total number of deleted users present in that group and ban them."
).info("Admin Menu").done()
    
