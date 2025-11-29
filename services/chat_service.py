# ============================================================
#  services/chat_service.py
#  Finagro AI — Agro + Kredit + Banking Chatbot
#  Model: gpt-4.1-mini (OpenAI)
# ============================================================

import random
from config import settings
from openai import OpenAI

# OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# ❌ Javob BERILMAYDIGAN mavzular (taqiqlangan)
FORBIDDEN_TOPICS = [
    "siyosat", "prezident", "hukumat", "diniy",
    "urush", "terror", "porn", "seks", "18+"
]

# 😂 Hazil bilan javob beriladigan maxsus mavzular
FUN_TOPICS = {
    "mars": "Marsni Elon Muskga qoldiramiz 🚀 Men esa hosilingizni osmonga ko‘taraman 😊",
    "sevgi": "Sevgi go‘zal narsa ❤️ Ammo hosil ham yaxshi bo‘lsa yurak tinch bo‘ladi 😊"
}

# ------------------- Forbidden tekshirish -------------------
def is_forbidden(message: str) -> bool:
    text = message.lower()
    return any(bad in text for bad in FORBIDDEN_TOPICS)

# ------------------- Fun topic aniqlash ---------------------
def detect_fun_topic(message: str):
    text = message.lower()
    for key in FUN_TOPICS:
        if key in text:
            return key
    return None

# ------------------------ OpenAI Call ------------------------
async def ask_model(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Siz Finagro AI Chatbotsiz. Qishloq xo‘jaligi, hosil, "
                    "kasalliklar, o‘g‘itlash, suv taqchilligi, agrotexnika, "
                    "Agrobank kreditlari va moliyaviy maslahatlar bo‘yicha "
                    "sodda, tushunarli va iliq ohangda javob bering."
                )
            },
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# ------------------------ Chatbot Logic ------------------------
async def handle_chat(message: str) -> dict:
    lower_msg = message.lower()

    # ❌ 1. Taqiqlangan mavzular
    if is_forbidden(lower_msg):
        return {
            "reply": (
                "Kechirasiz, bu mavzu bo‘yicha javob bera olmayman. "
                "Lekin hosil, o‘g‘itlash, suv taqchilligi yoki Agrobank krediti "
                "haqida bemalol so‘rashingiz mumkin 🌿"
            ),
            "bank_button": False
        }

    # 😂 2. Fun (Mars, sevgi, memlar...) — hazil bilan javob qaytaradi
    fun_key = detect_fun_topic(lower_msg)
    if fun_key:
        return {
            "reply": FUN_TOPICS[fun_key],
            "bank_button": False
        }

    # 🌱 3. Barcha boshqa mavzular — OpenAI orqali normal javob
    ai_reply = await ask_model(message)

    bank_button = any(
        word in lower_msg for word in ["kredit", "qarz", "foiz", "bank", "pul"]
    )

    return {
        "reply": ai_reply,
        "bank_button": bank_button
    }