# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routers.chat import router as chat_router

# Kredit bo‘limi
from kredit_hisoblash import hisobla_kredit
from pydantic import BaseModel


# -------------------- REQUEST MODEL --------------------
class KreditRequest(BaseModel):
    yer_maydoni_ha: float    
    ekin_turi: str           
    viloyat: str             
    zichlik: float           


# -------------------- FASTAPI APP ----------------------
app = FastAPI(
    title="Finagro AI API",
    description="Agro + Credit + Banking AI Assistant Backend",
    version="1.0.0"
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- ROOT ROUTE -----------------------
@app.get("/")
def home():
    return {"message": "Finagro AI API is running successfully!"}


# -------------------- CHAT ROUTES ----------------------
app.include_router(chat_router)


# -------------------- CREDIT API -----------------------
@app.post("/hosildan-kredit")
def kredit_api(request: KreditRequest):
    natija = hisobla_kredit(
        yer_maydoni_ha=request.yer_maydoni_ha,
        ekin_turi=request.ekin_turi,
        viloyat=request.viloyat,
        zichlik=request.zichlik,
    )
    return natija