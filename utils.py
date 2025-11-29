import re

# --- Matnni tozalash ---
def clean_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


# --- Off-topic javoblar (hazil bilan) ---
def get_offtopic_reply(user_msg: str) -> str:
    user_msg = user_msg.lower()

    off_map = {
        "mars": "Mars haqida Elon Musk yaxshi biladi 😄 Men esa sizning hosilingizni yerda ko‘tarishga yordam beraman.",
        "elon": "Elon haqida ko‘p eshitganman 😄 Lekin men sizning dalangizdan xabar olib turaman!",
        "sevaman": "Men sun'iy intellektman 😅 sevgi masalalarida ko‘p narsa bilmayman. Ammo paxtangizni juda yaxshi ko‘raman!",
        "kino": "Kino yaxshi narsa 😄 lekin men sizning hosilingizni oshirish bo‘yicha kuchliroqman!",
        "dollar": "Dollar kursini banklar aytadi 😄 Lekin hosilingiz qanchaga tushishini hisoblab bera olaman!"
    }

    for key in off_map:
        if key in user_msg:
            return off_map[key]

    return "Qiziq savol 😄 Ammo men faqat agro va kredit bo‘yicha yordam bera olaman."
