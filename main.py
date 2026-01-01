import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
import qrcode
from io import BytesIO

# Environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH"))
SESSION_STRING = os.getenv("SESSION_STRING")
BOT_NAME = os.getenv("BOT_NAME", "˹ 𝐀𝐐𝐔𝐀 ꭙ 𝐌ᴜsɪᴄ ˼")
OWNER_NAME = os.getenv("OWNER_NAME", "𝗧𝗛𝗘𝗚𝗔𝗠𝗘𝗥𝗔𝗗𝗘𝗣𝗧")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "@ENDLES_ERA")

# Userbot client
user = Client("userbot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
vc = PyTgCalls(user)

user.start()
vc.start()

# /start command
@user.on_message(filters.command("start"))
async def start(_, message):
    text = f"""
❖ ᴄυᴛє {BOT_NAME} ση sᴛʀєᴧϻɪηɢ ⏤͟͞●
❖ This is a Management & Music Bot
❖ No lag | Ads-free music | No promo
❖ 24x7 run | Best sound quality
"""
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add me in your Group", url=f"https://t.me/AquaXmusicBot?startgroup=true")],
        [InlineKeyboardButton("Updates", url="https://t.me/AQUAxMUSIC_UPDATES"),
         InlineKeyboardButton("Support", url="https://t.me/AQUAxMUSIC")],
        [InlineKeyboardButton("Owner", url=f"https://t.me/{OWNER_USERNAME[1:]}")]
    ])
    await message.reply(text, reply_markup=buttons)

# /play command
@user.on_message(filters.command("play") & filters.group)
async def play(_, message):
    query = " ".join(message.command[1:])
    ydl_opts = {"format": "bestaudio", "noplaylist": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        url = info["url"]
        title = info["title"]

    await vc.join_group_call(message.chat.id, AudioPiped(url))
    await message.reply(f"❖ ᴄυᴛє {BOT_NAME} streaming 🎵\n❍ Title ➥ {title}\n❍ By ➥ {message.from_user.first_name}\n❖ Made by ➛ {OWNER_NAME} ({OWNER_USERNAME})")

# /stop command
@user.on_message(filters.command("stop") & filters.group)
async def stop(_, message):
    await vc.leave_group_call(message.chat.id)
    await message.reply("Stopped streaming and left VC ✅")

# /id command
@user.on_message(filters.command("id"))
async def show_id(_, message):
    text = f"""
❖ Message ID: {message.message_id}
❖ Your ID: {message.from_user.id}
❖ Chat ID: {message.chat.id}
"""
    await message.reply(text)

# /qr command
@user.on_message(filters.command("qr"))
async def qr(_, message):
    if len(message.command) < 2:
        await message.reply("Usage: /qr <text or link>")
        return
    qr_text = " ".join(message.command[1:])
    img = qrcode.make(qr_text)
    bio = BytesIO()
    bio.name = "qr.png"
    img.save(bio, "PNG")
    bio.seek(0)
    await message.reply_photo(bio, caption=f"QR for: {qr_text}")

print("🚀 AQUAxMUSIC Userbot is online!")
user.idle()
