import random

from Hellbot import __version__
from Hellbot.core import ENV, db

ALIVE_TEMPLATES = [
    (
        "•────────────────•\n"
        "•       RinBᴏᴛ Is Aʟɪᴠᴇ        •\n"
        "╭────────────────•\n"
        "╰➢ ᴏᴡɴᴇʀ » {owner}\n"
        "╰➢ ᴘʏʀᴏɢʀᴀᴍ » {pyrogram}\n"
        "╰➢ ʜᴇʟʟʙᴏᴛ » {hellbot}\n"
        "╰➢ ᴘʏᴛʜᴏɴ » {python}\n"
        "╰➢ ᴜᴘᴛɪᴍᴇ » {uptime}\n"
        "╰────────────────•\n"
        "By © @Chowdhury_Siam\n"
        "•────────────────•\n"
    ),
]

PING_TEMPLATES = [
    """**🍀 Ping!**

    ⚘  **ѕρєє∂:** {speed} m/s
    ⚘  **υρтιмє:** {uptime}
    ⚘  **σωηєя:** {owner}""",
]

HELP_MENU_TEMPLATES = [
    """**🍀 Help Menu for:** {owner}

__📃 Loaded__ **{plugins} plugins** __with a total of__ **{commands} commands.**

**📑 Page:** __{current}/{last}__""",
]

COMMAND_MENU_TEMPLATES = [
    """**Plugin File:** `{file}`
**Plugin Info:** __{info} 🍀__

**📃 Loaded Commands:** `{commands}`""",
]

ANIME_TEMPLATES = [
    """
{name}

╭────────────────•
╰➢ **Score:** `{score}`
╰➢ **Source:** `{source}`
╰➢ **Type:** `{mtype}`
╰➢ **Episodes:** `{episodes}`
╰➢ **Duration:** `{duration} minutes`
╰➢ **Status:** `{status}`
╰➢ **Format:** `{format}`
╰➢ **Genre:** `{genre}`
╰➢ **Tags:** `{tags}`
╰➢ **Adult Rated:** `{isAdult}`
╰➢ **Studio:** `{studio}`
╰➢ **Trailer:** {trailer}
╰➢ **Website:** {siteurl}
╰➢ **Synopsis:** [Click Here]({description})
╰────────────────•
"""
]

MANGA_TEMPLATES = [
    """
{name}

╭────────────────•
╰➢ **Score:** `{score}`
╰➢ **Source:** `{source}`
╰➢ **Type:** `{mtype}`
╰➢ **Chapters:** `{chapters}`
╰➢ **Volumes:** `{volumes}`
╰➢ **Status:** `{status}`
╰➢ **Format:** `{format}`
╰➢ **Genre:** `{genre}`
╰➢ **Adult Rated:** `{isAdult}`
╰➢ **Website:** {siteurl}
╰➢ **Synopsis:** [Click Here]({description})
╰────────────────•
"""
]

CHARACTER_TEMPLATES = [
    """
{name}

╭────────────────•
╰➢ **Gender:** `{gender}`
╰➢ **Date of Birth:** `{date_of_birth}`
╰➢ **Age:** `{age}`
╰➢ **Blood Type:** `{blood_type}`
╰➢ **Favourites:** `{favorites}`
╰➢ **Website:** {siteurl}{role_in}
╰────────────────•
{description}
"""
]

AIRING_TEMPLATES = [
    """
{name}

╭────────────────•
╰➢ **Status:** `{status}`
╰➢ **Episode:** `{episode}`
╰────────────────•{airing_info}
"""
]

ANILIST_USER_TEMPLATES = [
    """
**💫 {name}**

╭──── Anime ─────•
╰➢ **Count:** `{anime_count}`
╰➢ **Score:** `{anime_score}`
╰➢ **Minutes Spent:** `{minutes}`
╰➢ **Episodes Watched:** `{episodes}`
╰────────────────•
╭──── Manga ─────•
╰➢ **Count:** `{manga_count}`
╰➢ **Score:** `{manga_score}`
╰➢ **Chapters:** `{chapters}`
╰➢ **Volumes:** `{volumes}`
╰────────────────•

Website: {siteurl}
"""
]

CLIMATE_TEMPLATES = [
    """
🌆 {city_name}, {country}

╭────────────────•
╰➢ **Weather:** {weather}
╰➢ **Timezone:** {timezone}
╰➢ **Sunrise:** {sunrise}
╰➢ **Sunset:** {sunset}
╰➢ **Wind:** {wind}
╰➢ **Temperature:** {temperature}°C
╰➢ **Feels like:** {feels_like}°C
╰➢ **Minimum:** {temp_min}°C
╰➢ **Maximum:** {temp_max}°C
╰➢ **Pressure:** {pressure} hPa
╰➢ **Humidity:** {humidity}%
╰➢ **Visibility:** {visibility} m
╰➢ **Clouds:** {clouds}%
╰────────────────•
"""
]

AIR_POLLUTION_TEMPLATES = [
    """
🌆 {city_name}

╭────────────────•
╰➢ **AQI:** {aqi}
╰➢ **Carbon Monoxide:** {co}
╰➢ **Noitrogen Monoxide:** {no}
╰➢ **Nitrogen Dioxide:** {no2}
╰➢ **Ozone:** {o3}
╰➢ **Sulphur Dioxide:** {so2}
╰➢ **Ammonia:** {nh3}
╰➢ **Fine Particles (PM{sub2_5}):** {pm2_5}
╰➢ **Coarse Particles (PM{sub10}):** {pm10}
╰────────────────•
"""
]

GITHUB_USER_TEMPLATES = [
    """
🍀 {username} ({git_id})

╭──────── {id_type} ────────•
╰➢ **Name:** [{name}]({profile_url})
╰➢ **Blog:** {blog}
╰➢ **Company:** {company}
╰➢ **Email:** {email}
╰➢ **Location:** {location}
╰➢ **Repo:** {public_repos}
╰➢ **Gists:** {public_gists}
╰➢ **Followers:** {followers}
╰➢ **Following:** {following}
╰➢ **Account created:** {created_at}
╰────────────────•

**💫 Bio:** {bio}
"""
]

STATISTICS_TEMPLATES = [
    """
🍀 {name}

╭──────── Channels ────────•
╰➢ **Total:** `{channels}`
╰➢ **Admin:** `{ch_admin}`
╰➢ **Owner:** `{ch_owner}`

╭──────── Groups ────────•
╰➢ **Total:** `{groups}`
╰➢ **Admin:** `{gc_admin}`
╰➢ **Owner:** `{gc_owner}`

╭──────── Others ────────•
╰➢ **Private:** `{users}`
╰➢ **Bots:** `{bots}`
╰➢ **Unread Messages:** `{unread_msg}`
╰➢ **Unread Mentions:** `{unread_mention}`

⌛ **Time Taken:** `{time_taken}`
"""
]

GBAN_TEMPLATES = [
    """
╭──────── {gtype} ────────•
╰➢ **Victim:** {name}
╰➢ **Success:** {success}
╰➢ **Failed:** {failed}
╰➢ **Reason:** {reason}
╰────────────────•
"""
]

USAGE_TEMPLATES = [
    """
**📝 Disk & Dyno Usage:**

**➢ Dyno Usage for** `{appName}`
    ◈ __{appHours}hrs {appMinutes}mins__ | __{appPercentage}%__

**➢ Dyno remaining this month:**
    ◈ __{hours}hrs {minutes}mins__ | __{percentage}%__

**➢ Disk Usage:**
    ◈ __{diskUsed}GB__ / __{diskTotal}GB__ | __{diskPercent}%__

**➢ Memory Usage:**
    ◈ __{memoryUsed}GB__ / __{memoryTotal}GB__ | __{memoryPercent}%__
"""
]

USER_INFO_TEMPLATES = [
    """
**🍀 User Info of {mention}:**

**➢ First Name:** `{firstName}`
**➢ Last Name:** `{lastName}`
**➢ UserID:** `{userId}`

**➢ Common Groups:** `{commonGroups}`
**➢ DC-ID:** `{dcId}`
**➢ Pictures:** `{totalPictures}`
**➢ Restricted:** `{isRestricted}`
**➢ Verified:** `{isVerified}`
**➢ Bot:** `{isBot}`
**➢ Bio:** `{bio}`

**</> @Chowdhury_Siam**
"""
]

CHAT_INFO_TEMPLATES = [
    """
**🍀 Chat Info:**

**➢ Chat Name:** `{chatName}`
**➢ Chat ID:** `{chatId}`
**➢ Chat Link:** {chatLink}
**➢ Owner:** {chatOwner}
**➢ DC-ID:** `{dcId}`
**➢ Members:** `{membersCount}`
**➢ Admins:** `{adminsCount}`
**➢ Bots:** `{botsCount}`
**➢ Description:** `{description}`

**</> @Chowdhury_Siam**
"""
]


async def alive_template(owner: str, uptime: str) -> str:
    template = await db.get_env(ENV.alive_template)
    if template:
        message = template
    else:
        message = random.choice(ALIVE_TEMPLATES)
    return message.format(
        owner=owner,
        pyrogram=__version__["pyrogram"],
        hellbot=__version__["hellbot"],
        python=__version__["python"],
        uptime=uptime,
    )


async def ping_template(speed: float, uptime: str, owner: str) -> str:
    template = await db.get_env(ENV.ping_template)
    if template:
        message = template
    else:
        message = random.choice(PING_TEMPLATES)
    return message.format(speed=speed, uptime=uptime, owner=owner)


async def help_template(
    owner: str, cmd_n_plgn: tuple[int, int], page: tuple[int, int]
) -> str:
    template = await db.get_env(ENV.help_template)
    if template:
        message = template
    else:
        message = random.choice(HELP_MENU_TEMPLATES)
    return message.format(
        owner=owner,
        commands=cmd_n_plgn[0],
        plugins=cmd_n_plgn[1],
        current=page[0],
        last=page[1],
    )


async def command_template(file: str, info: str, commands: str) -> str:
    template = await db.get_env(ENV.command_template)
    if template:
        message = template
    else:
        message = random.choice(COMMAND_MENU_TEMPLATES)
    return message.format(file=file, info=info, commands=commands)


async def anime_template(**kwargs) -> str:
    template = await db.get_env(ENV.anime_template)
    if template:
        message = template
    else:
        message = random.choice(ANIME_TEMPLATES)
    return message.format(**kwargs)


async def manga_templates(**kwargs) -> str:
    template = await db.get_env(ENV.manga_template)
    if template:
        message = template
    else:
        message = random.choice(MANGA_TEMPLATES)
    return message.format(**kwargs)


async def character_templates(**kwargs) -> str:
    template = await db.get_env(ENV.character_template)
    if template:
        message = template
    else:
        message = random.choice(CHARACTER_TEMPLATES)
    return message.format(**kwargs)


async def airing_templates(**kwargs) -> str:
    template = await db.get_env(ENV.airing_template)
    if template:
        message = template
    else:
        message = random.choice(AIRING_TEMPLATES)
    return message.format(**kwargs)


async def anilist_user_templates(
    name: str, anime: tuple, manga: tuple, siteurl: str
) -> str:
    template = await db.get_env(ENV.anilist_user_template)
    if template:
        message = template
    else:
        message = random.choice(ANILIST_USER_TEMPLATES)
    return message.format(
        name=name,
        anime_count=anime[0],
        anime_score=anime[1],
        minutes=anime[2],
        episodes=anime[3],
        manga_count=manga[0],
        manga_score=manga[1],
        chapters=manga[2],
        volumes=manga[3],
        siteurl=siteurl,
    )


async def climate_templates(**kwargs) -> str:
    template = await db.get_env(ENV.climate_template)
    if template:
        message = template
    else:
        message = random.choice(CLIMATE_TEMPLATES)
    return message.format(**kwargs)


async def airpollution_templates(**kwargs) -> str:
    template = await db.get_env(ENV.airpollution_template)
    if template:
        message = template
    else:
        message = random.choice(AIR_POLLUTION_TEMPLATES)
    return message.format(**kwargs)


async def statistics_templates(**kwargs) -> str:
    template = await db.get_env(ENV.statistics_template)
    if template:
        message = template
    else:
        message = random.choice(STATISTICS_TEMPLATES)
    return message.format(**kwargs)


async def github_user_templates(**kwargs) -> str:
    template = await db.get_env(ENV.github_user_template)
    if template:
        message = template
    else:
        message = random.choice(GITHUB_USER_TEMPLATES)
    return message.format(**kwargs)


async def gban_templates(**kwargs) -> str:
    template = await db.get_env(ENV.gban_template)
    if template:
        message = template
    else:
        message = random.choice(GBAN_TEMPLATES)
    return message.format(**kwargs)


async def usage_templates(**kwargs) -> str:
    template = await db.get_env(ENV.usage_template)
    if template:
        message = template
    else:
        message = random.choice(USAGE_TEMPLATES)
    return message.format(**kwargs)


async def user_info_templates(**kwargs) -> str:
    template = await db.get_env(ENV.user_info_template)
    if template:
        message = template
    else:
        message = random.choice(USER_INFO_TEMPLATES)
    return message.format(**kwargs)


async def chat_info_templates(**kwargs) -> str:
    template = await db.get_env(ENV.chat_info_template)
    if template:
        message = template
    else:
        message = random.choice(CHAT_INFO_TEMPLATES)
    return message.format(**kwargs)
