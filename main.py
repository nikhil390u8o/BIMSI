from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
import asyncio
import os

API_ID = 20898349
API_HASH = "9fdb830d1e435b785f536247f49e7d87"
STRING_SESSION = "BQE-4i0ApUkY5_ljChHwN3MwsOB7GNrxEQcXhXW0sLKzHZlkJH4i8TdVEAOmsuqwKYbrIfKgw6XGHEOkS2b3TFmQeVZCcDPd06MVqnO-81QGM_DwwW9CQN6YhPwVFlRLw8Gllu44_PaaD8fFZyg7O2YOAawg7r4nA5v6oJ_uaFyFGpohtMYzLO27COjkeId1V5qWXy-t5qq6d3J8ZbeFHtwNM8OhI9rHA4xCLJNC4sAD6WqwkKbR6sM-UGGGl4gR95gYnSvkesN6L3wnzuQ4ADQJ1kUrP_TITYpDlZBSOpdFKPcQA0SrmQNqWyipAtCaHh5IYPPCMrWVXMDOeFttZg31U4WYGAAAAAHKarFXAA"

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
