import asyncio

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from Hellbot.core import LOGS

from . import HelpMenu, custom_handler, db, group_only, handler, hellbot, on_message


@on_message(
    "promote",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
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
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=True,
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
    admin_only=True,
    allow_stan=True,
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
    ["ban", "dban"],
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def ban(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) < 2:
            reason = None
        else:
            reason = await hellbot.input(message)
        if message.command[0][0].lower() == "d":
            await message.reply_to_message.delete()
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
    ["nuke", "dnuke"],
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def nuke(client: Client, message: Message):
    # Ensure the command contains at least channel_id and user_id
    if len(message.command) < 3:
        return await hellbot.delete(message, "Please provide both a channel ID and user ID.")

    try:
        # Extract the channel ID and user ID from the command arguments
        channel_id = int(message.command[1])
        user_id = int(message.command[2])

        # If there's an additional argument, treat it as the reason
        reason = await hellbot.input(message) if len(message.command) > 3 else None

        # Get the channel and ensure it's valid
        chat = await client.get_chat(channel_id)

        # Nuke (ban) the user in the specified channel
        await client.ban_chat_member(chat.id, user_id)

        # Delete the message after nuking the user
        if message.command[0][0].lower() == "d":
            await message.reply_to_message.delete()

        # Respond with a success message
        reason = reason if reason else "Not Specified"
        await hellbot.delete(
            message,
            f"**☠️ Nuked User ID {user_id} successfully from {chat.title}!**\n**Reason:** `{reason}`",
            30,
        )
        await hellbot.check_and_log(
            "nuke",
            f"**Nuked User**\n\n**User ID:** `{user_id}`\n**Reason:** `{reason}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{chat.title}`\n**Group ID:** `{chat.id}`",
        )
    except Exception as e:
        await hellbot.error(message, f"Failed to nuke user: {e}")



@on_message(
    "unban",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
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
    ["kick", "dkick"],
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def kick(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) < 2:
            reason = None
        else:
            reason = await hellbot.input(message)
        if message.command[0][0].lower() == "d":
            await message.reply_to_message.delete()
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
    admin_only=True,
    allow_stan=True,
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
        message,
        f"**🤐 Muted {user.mention} Successfully!**\n**Reason:** `{reason}`",
        30,
    )
    await hellbot.check_and_log(
        "mute",
        f"**Muted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unmute",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
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


@on_message("dmute", allow_stan=True)
async def dmute(client: Client, message: Message):
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

    if await db.is_muted(client.me.id, user.id, message.chat.id):
        return await hellbot.delete(message, "This user is already dmuted.")

    reason = reason if reason else "Not Specified"
    await db.add_mute(client.me.id, user.id, message.chat.id, reason)
    await hellbot.delete(
        message,
        f"**🤐 Muted {user.mention} Successfully!**\n**Reason:** `{reason}`",
        30,
    )
    await hellbot.check_and_log(
        "dmute",
        f"**D-Muted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title or message.chat.first_name}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message("undmute", allow_stan=True)
async def undmute(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, "Need a username/id or reply to a user to unmute them!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    if not await db.is_muted(client.me.id, user.id, message.chat.id):
        return await hellbot.delete(message, "The user is not muted!")

    reason = await db.rm_mute(client.me.id, user.id, message.chat.id)
    await hellbot.delete(
        message,
        f"**😁 Unmuted {user.mention} Successfully!**\n\n**Mute reason was:** `{reason}`",
        30,
    )
    await hellbot.check_and_log(
        "unmute",
        f"**D-Unmuted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "pin",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
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
    admin_only=True,
    allow_stan=True,
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
    admin_only=True,
    allow_stan=True,
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


@custom_handler(filters.incoming)
async def multiple_handler(client: Client, message: Message):
    if not message.from_user:
        return

    if await db.is_muted(client.me.id, message.from_user.id, message.chat.id):
        try:
            await message.delete()
        except:
            pass

    elif await db.is_gmuted(message.from_user.id):
        try:
            await message.delete()
        except:
            pass

    elif await db.is_echo(client.me.id, message.chat.id, message.from_user.id):
        await message.copy(message.chat.id, reply_to_message_id=message.id)


HelpMenu("admin").add(
    "promote",
    "<username/id/reply> <title>",
    "Promote a user to admin.",
    "promote @ForGo10God hellboy",
).add(
    "demote", "<username/id/reply>", "Demote a user from admin.", "demote @ForGo10God"
).add(
    "ban",
    "<username/id/reply> <reason>",
    "Ban a user from the group.",
    "ban @ForGo10God",
    "You can also use dban to delete the message of the user.",
).add(
    "nuke",
    "<channel id> <username/id/reply> <reason>",
    "Ban a user from the channel.",
    "nuke -100iudiewdi ForGo10God",
    "You can also use dban to delete the message of the user.",
).add(
    "unban", "<username/id/reply>", "Unban a user from the group.", "unban @ForGo10God"
).add(
    "kick",
    "<username/id/reply> <reason>",
    "Kick a user from the group.",
    "kick @ForGo10God",
    "You can also use dkick to delete the message of the user.",
).add(
    "mute",
    "<username/id/reply> <reason>",
    "Mute a user in the group",
    "mute @ForGo10God",
    "You can also use dmute to delete the message of the user.",
).add(
    "unmute", "<username/id/reply>", "Unmute a user in the group.", "unmute @ForGo10God"
).add(
    "dmute",
    "<username/id/reply>",
    "Mute a user by deleting their new messages in the group.",
    "dmute @ForGo10God",
    "Need delete message permission for proper functioning.",
).add(
    "undmute",
    "<username/id/reply>",
    "Unmute a user who's muted using 'dmute' command in the group.",
    "undmute @ForGo10God",
).add(
    "pin", "<reply>", "Pin the replied message in the group."
).add(
    "unpin", "<reply>", "Unpin the replied pinned message in the group."
).add(
    "zombies",
    "clean",
    "Finds the total number of deleted users present in that group and ban them.",
).info(
    "Admin Menu"
).done()
