from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import json
import os
from pathlib import Path

router = APIRouter(prefix="/auth", tags=["auth"])

# User JSON file yo'li
USERS_FILE = Path("public/user.json")

class UserLogin(BaseModel):
    email: str
    password: str

class UserSignUp(BaseModel):
    name: str
    email: str
    password: str

def load_users():
    """User data ni JSON file dan yuklash"""
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("users", [])
    return []

def save_users(users):
    """User data ni JSON file ga saqlash"""
    os.makedirs(USERS_FILE.parent, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, indent=2, ensure_ascii=False)

@router.post("/login")
def login(credentials: UserLogin):
    """User login - email va parol tekshiruvi"""
    users = load_users()
    
    user = next((u for u in users if u["email"] == credentials.email and u["password"] == credentials.password), None)
    
    if not user:
        raise HTTPException(status_code=401, detail="Email yoki parol noto'g'ri!")
    
    # Akkaunt mavjud va parol to'g'ri
    return {
        "success": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        },
        "message": "Muvaffaqiyatli kirdingiz!"
    }

@router.post("/signup")
def signup(user_data: UserSignUp):
    """User signup - yangi akkaunt yaratish"""
    users = load_users()
    
    # Email allaqachon ro'yxatdan o'tganmi?
    if any(u["email"] == user_data.email for u in users):
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro'yxatdan o'tgan!")
    
    # Parol uzunligi tekshiruvi
    if len(user_data.password) < 8:
        raise HTTPException(status_code=400, detail="Parol kamita 8 ta belgidan iborat bo'lishi kerak!")
    
    # Yangi user yaratish
    new_user = {
        "id": len(users) + 1,
        "name": user_data.name,
        "email": user_data.email,
        "password": user_data.password,
        "registrationTime": __import__("datetime").datetime.now().isoformat() + "Z"
    }
    
    users.append(new_user)
    save_users(users)
    
    return {
        "success": True,
        "user": {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"]
        },
        "message": "Akkaunt muvaffaqiyatli yaratildi!"
    }

@router.get("/check-auth")
def check_auth():
    """Auth status tekshiruvi"""
    return {"message": "Auth endpoint faol"}
