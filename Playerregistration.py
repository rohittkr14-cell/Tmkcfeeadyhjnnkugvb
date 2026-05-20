# =========================================
#        TELEGRAM CRICKET BOT
# =========================================

# INSTALL:
# pip install pyrogram tgcrypto

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import json
import os

# =========================================
# CONFIG
# =========================================

API_ID = 37893084
API_HASH = "853a6c0f3be11009f667bc153244452e"
BOT_TOKEN = "8867725715:AAF_i-FTBbBFC6WiRFKy2Jbu_WoR4YyR_R0"

BOT_NAME = "PREMIUM LEAGUE"

# =========================================
# DATABASE
# =========================================

DB_FILE = "players.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =========================================
# DEFAULT PLAYER
# =========================================

def default_player(role):

    return {
        "role": role,
        "exp": 0,

        "highest": 0,
        "balls": 0,
        "runs": 0,

        "avg": "0.00",
        "sr": "0.00",

        "six": 0,
        "four": 0,

        "hundred": 0,
        "fifty": 0,

        "ducks": 0,

        "wickets": 0,
        "hattrick": 0,

        "overs": "0.0",
        "eco": "0.00",

        "solo": 0,
        "team": 0,

        "motm": 0
    }

# =========================================
# PROFILE TEXT
# =========================================

def profile_text(user, data):

    exp = data.get("exp", 0)

    need = 1000 - exp

    return f"""
📊 <b>PROFILE 🔰 STATISTICS</b>

═══════════════
👤 <b>Name:</b> {user.first_name}
🆔 <b>ID:</b> {user.id}
🏏 <b>Role:</b> {data.get("role").upper()}

⭐ <b>EXP:</b> {exp}
⚡ <b>Next:</b> Pro ({need} EXP Left)

═══════════════
🏏 <b>BATTING</b>

🔸 <b>Highest:</b> {data.get("highest")} ({data.get("balls")})
🔸 <b>Runs:</b> {data.get("runs")}
🔸 <b>Avg:</b> {data.get("avg")}
🔸 <b>SR:</b> {data.get("sr")}

🔸 <b>6s:</b> {data.get("six")}
🔸 <b>4s:</b> {data.get("four")}

🔸 <b>100s:</b> {data.get("hundred")}
🔸 <b>50s:</b> {data.get("fifty")}
🔸 <b>Ducks:</b> {data.get("ducks")}

═══════════════
🥎 <b>BOWLING</b>

🔹 <b>Wickets:</b> {data.get("wickets")}
🔹 <b>Hat-Tricks:</b> {data.get("hattrick")}
🔹 <b>Overs:</b> {data.get("overs")}
🔹 <b>Economy:</b> {data.get("eco")}

═══════════════
🏆 <b>MATCHES</b>

🔸 <b>Solo:</b> {data.get("solo")}
🔸 <b>Team:</b> {data.get("team")}
🔸 <b>MOTM:</b> {data.get("motm")}

═══════════════
"""

# =========================================
# GET PROFILE PHOTO
# =========================================

async def get_profile_photo(user):

    try:

        photos = []

        async for photo in app.get_chat_photos(user.id, limit=1):
            photos.append(photo.file_id)

        # USER PROFILE PHOTO
        if photos:
            return photos[0]

        # NAME AVATAR
        return f"https://ui-avatars.com/api/?name={user.first_name}&background=random"

    except:

        return f"https://ui-avatars.com/api/?name={user.first_name}&background=random"

# =========================================
# BOT CLIENT
# =========================================

app = Client(
    "cricket_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================================
# START COMMAND
# =========================================

@app.on_message(filters.command("start"))
async def start(client, message):

    user = message.from_user
    user_id = str(user.id)

    db = load_data()

    profile_photo = await get_profile_photo(user)

    # =====================================
    # REGISTERED USER
    # =====================================

    if user_id in db:

        text = profile_text(user, db[user_id])

        await message.reply_photo(
            photo=profile_photo,
            caption=text
        )

        return

    # =====================================
    # NEW USER
    # =====================================

    text = f"""
🏏 <b>WELCOME TO {BOT_NAME}</b>

🔥 Enter the official Premium league.

📌 <b>Available Roles:</b>

🏏 <b>Batsman</b>
🎯 <b>Bowler</b>
⚡ <b>All Rounder</b>

👇 <b>Register Below</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Register",
                    callback_data="register"
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="cancel"
                )
            ]
        ]
    )

    await message.reply_photo(
        photo=profile_photo,
        caption=text,
        reply_markup=buttons
    )

# =========================================
# CANCEL BUTTON
# =========================================

@app.on_callback_query(filters.regex("cancel"))
async def cancel(client, query):

    await query.message.delete()

# =========================================
# REGISTER BUTTON
# =========================================

@app.on_callback_query(filters.regex("register"))
async def register(client, query):

    user_id = str(query.from_user.id)

    db = load_data()

    # =====================================
    # ALREADY REGISTERED
    # =====================================

    if user_id in db:

        role = db[user_id]["role"]

        await query.answer(
            f"Already Registered as {role.upper()}",
            show_alert=True
        )

        return

    text = """
🏏 <b>SELECT YOUR ROLE</b>

👇 <b>Choose Below</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🏏 Batsman",
                    callback_data="role_batsman"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎯 Bowler",
                    callback_data="role_bowler"
                )
            ],
            [
                InlineKeyboardButton(
                    "⚡ All Rounder",
                    callback_data="role_allrounder"
                )
            ]
        ]
    )

    await query.message.edit_caption(
        caption=text,
        reply_markup=buttons
    )

# =========================================
# ROLE SELECT
# =========================================

@app.on_callback_query(filters.regex("role_"))
async def role_select(client, query):

    user = query.from_user
    user_id = str(user.id)

    db = load_data()

    # =====================================
    # ALREADY REGISTERED
    # =====================================

    if user_id in db:

        await query.answer(
            "Already Registered!",
            show_alert=True
        )

        return

    # =====================================
    # SAVE ROLE
    # =====================================

    role = query.data.replace("role_", "")

    db[user_id] = default_player(role)

    save_data(db)

    profile_photo = await get_profile_photo(user)

    text = profile_text(user, db[user_id])

    await query.message.delete()

    await query.message.reply_photo(
        photo=profile_photo,
        caption=text
    )

# =========================================
# RUN BOT
# =========================================

print("🏏 Cricket Bot Started Successfully")

app.run()