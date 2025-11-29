# kredit_hisoblash.py
# Finagro AI — Hosildan Kredit hisoblash moduli (MVP)
# Backend (FastAPI) + CLI uchun umumiy funksiya

from typing import Dict


# --- 1. Ichki ma'lumotlar (oddiy MVP model) ---

# 1 kg / 1 t narxlar (shunchaki taxminiy qiymatlar, hackathon MVP uchun)
EKIN_NARXLARI = {
    "paxta": 8000,      # so'm / kg (yoki ekvivalent)
    "galla": 3500,
    "pomidor": 2500,
    "kartoshka": 4000,
    "sabzi": 3000,
}

# Gektar boshiga bazaviy hosil koeffitsienti (oddiy model)
HOSIL_KOEFF = {
    "paxta": 2.1,       # t/ga (baza)
    "galla": 3.5,
    "pomidor": 12,
    "kartoshka": 18,
    "sabzi": 22,
}

# Viloyat bo‘yicha bonus koeffitsientlar
VILOYAT_BONUS = {
    "toshkent": 1.05,
    "samarqand": 1.07,
    "jizzax": 1.03,
    "andijon": 1.09,
    "fargona": 1.08,
    "farg‘ona": 1.08,
    "namangan": 1.07,
    "buxoro": 1.02,
    "qashqadaryo": 1.03,
    "surxondaryo": 1.04,
    "navoiy": 0.98,
    "xorazm": 1.06,
    "qoraqalpogiston": 0.97,
    "qoraqalpog‘iston": 0.97,
}


def _normalize(text: str) -> str:
    """
    Matnni pastga aylantirish, bo‘sh joylarni tozalash va
    oddiy apostroflarni yagona ko‘rinishga keltirish.
    """
    t = text.strip().lower()
    # ' va ’ va ` larni bir xil ko‘rinishga keltiramiz
    t = (
        t.replace("'", "‘")
         .replace("`", "‘")
         .replace("’", "‘")
    )
    return t


def hisobla_kredit(
    yer_maydoni_ha: float,
    ekin_turi: str,
    viloyat: str,
    zichlik: float
) -> Dict[str, float]:
    """
    Asosiy kredit hisoblash funksiyasi (backend + CLI uchun).
    
    Kirish parametrlari:
      - yer_maydoni_ha: yer maydoni (gektar)
      - ekin_turi: "paxta", "galla", "pomidor", "kartoshka", "sabzi"
      - viloyat: masalan "toshkent", "andijon", "fargona" va h.k.
      - zichlik: ekin zichligi (%) – 0 dan 200 gacha taxminiy diapazon
    
    Natija:
      {
        "taxminiy_hosil_t": ...,
        "taxminiy_daromad": ...,
        "kredit_miqdori": ...
      }
    """

    # --- 0. Bazaviy validatsiya (MVP uchun yetarli darajada) ---

    if yer_maydoni_ha <= 0:
        raise ValueError("Yer maydoni 0 dan katta bo‘lishi kerak.")

    if zichlik <= 0 or zichlik > 200:
        # MVP uchun oddiy diapazon cheklovi
        raise ValueError("Zichlik foizi 0–200% oralig‘ida bo‘lishi kerak.")

    ekin_turi_norm = _normalize(ekin_turi)
    viloyat_norm = _normalize(viloyat)

    if ekin_turi_norm not in HOSIL_KOEFF or ekin_turi_norm not in EKIN_NARXLARI:
        raise ValueError(
            "Bunday ekin turi bazada yo‘q. "
            "Mavjud ekinlar: paxta, galla, pomidor, kartoshka, sabzi."
        )

    if viloyat_norm not in VILOYAT_BONUS:
        raise ValueError(
            "Viloyat noto‘g‘ri kiritilgan. "
            "Masalan: toshkent, andijon, fargona, samarqand va h.k."
        )

    # --- 1. Baza koeffitsientlarini olish ---
    baza_hosil = HOSIL_KOEFF[ekin_turi_norm]          # t/ga
    vil_koeff = VILOYAT_BONUS[viloyat_norm]
    narx_kg = EKIN_NARXLARI[ekin_turi_norm]

    # --- 2. Taxminiy hosil (tonna) ---
    # yer_maydoni_ha * baza_hosil * vil_koeff * (zichlik / 100)
    taxminiy_hosil_t = yer_maydoni_ha * baza_hosil * vil_koeff * (zichlik / 100)

    # --- 3. Taxminiy daromad ---
    # Oddiy model: 1 t ~ 1000 kg deb hisoblaymiz
    umumiy_daromad = taxminiy_hosil_t * 1000 * narx_kg

    # --- 4. Kredit hajmi (MVP formulasi) ---
    # Masalan, umumiy daromadning 40% qismi kredit sifatida tavsiya qilinadi.
    kredit_miqdori = umumiy_daromad * 0.4

    return {
        "taxminiy_hosil_t": round(taxminiy_hosil_t, 2),
        "taxminiy_daromad": round(umumiy_daromad, 2),
        "kredit_miqdori": round(kredit_miqdori, 2),
    }


# ==============================
# CLI VERSION (Terminalda ishlaydi)
# ==============================
if __name__ == "__main__":
    print("\n📌 Finagro AI — Hosildan Kredit Hisoblash (CLI versiya)\n")

    try:
        yer = float(input("Yer maydoni (ga): "))
        ekin = input("Ekin turi (paxta/galla/pomidor/kartoshka/sabzi): ")
        vil = input("Viloyat nomi (masalan: toshkent, samarqand...): ")
        zich = float(input("Ekin zichligi (%): "))

        natija = hisobla_kredit(yer, ekin, vil, zich)

        print("\n--- NATIJA ---")
        print("Taxminiy hosil (tonna):", natija["taxminiy_hosil_t"])
        print("Taxminiy daromad (so'm):", natija["taxminiy_daromad"])
        print("Berilishi mumkin bo‘lgan kredit (so'm):", natija["kredit_miqdori"])
        print("----------------------\n")

    except ValueError as e:
        print(f"\nXatolik: {e}\n")
    except Exception as e:
        print(f"\nKutilmagan xatolik: {e}\n")
