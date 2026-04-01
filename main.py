from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
import asyncio
import os

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "")

app = Client("vc_bot", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
call_py = PyTgCalls(app)

def get_mic_stream():
    return AudioPiped(
        "pipe:0",
        HighQualityAudio(),
        additional_ffmpeg_parameters=(
            "-f alsa -i default "
            "-filter:a 'volume=4.0,"
            "asetrate=48000*1.3,"
            "atempo=0.77,"
            "aresample=48000'"
        )
    )

@app.on_message(filters.command("join", prefixes=".") & filters.group)
async def join_vc(_, message: Message):
    chat_id = message.chat.id
    try:
        await call_py.join_group_call(chat_id, get_mic_stream())
        await message.reply("🎙️ Joined! Awaaz boost + high pitch ho rahi hai!")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@app.on_message(filters.command("leave", prefixes=".") & filters.group)
async def leave_vc(_, message: Message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply("👋 Left VC.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

async def main():
    await app.start()
    await call_py.start()
    print("✅ Bot running...")
    await idle()

asyncio.run(main())
