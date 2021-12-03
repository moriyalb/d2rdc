# coding: utf-8

from fastapi import FastAPI
from typing import Optional

app = FastAPI()
from src.db import LocalDatabase
db = LocalDatabase()

from src.cache import MemCache
cache = MemCache()

def check_user(token):
    return cache.get_user(token)

def check_super_user(token):
    uid = cache.get_user(token)
    if not uid:
        return False
    return db.is_super_user(uid)

@app.on_event("startup")
async def startup_event():
    pass
    
@app.on_event("shutdown")
async def shutdown_event():
    cache.shutdown()
    

@app.get("/")
def on_root():
    return {"result": "invalid route"}

#http://127.0.0.1:8000/user/register/m/111
@app.get("/user/register/{uid}/{pwdmd5}")
def on_user_register(uid: str, pwdmd5: str):
    print("On User Register -> ", uid, pwdmd5)
    if not uid or not pwdmd5:
        return {"result": "invalid user or user pwd"}
    
    if db.is_user_exists(uid):
        return {"result": "user is already registered"}

    db.add_candidate(uid, pwdmd5)
    return {"result": "ok"}

#http://127.0.0.1:8000/user/login/mario/b32d73e56ec99bc5ec8f83871cde708a
@app.get("/user/login/{uid}/{pwdmd5}")
def on_user_login(uid: str, pwdmd5: str):
    if not db.is_user_valid(uid, pwdmd5):
        return {"result": "invalid user"}

    token = cache.on_user_login(uid)
    return {"result": "ok", "token": token}

#http://127.0.0.1:8000/user/handle/m/refuse?token=48d537d3e4f545159143a68fb953ffe0
#http://127.0.0.1:8000/user/handle/m/agree?token=77722c3262e74d3d926fa54359f88a94
@app.get("/user/handle/{uid}/{agree}")
def on_user_handle(uid: str, agree: str, token: str):
    if not check_super_user(token):
        return {"result": "not super user"}

    agree = agree == "agree"
    if not agree:
        if db.delete_user(uid):
            return {"result": "ok"}
    else:
        if db.handle_candidate(uid):
            return {"result": "ok"}

    return {"result": "fail"}

#http://127.0.0.1:8000/user/delete/m?token=c33c80d729d84411a51e1b8b4a508728
@app.get("/user/delete/{uid}")
def on_user_delete(uid: str, token: str):
    if not check_super_user(token):
        return {"result": "not super user"}

    if db.delete_user(uid):
        return {"result": "ok"}

    return {"result": "fail"}

@app.get("/game/{game_ip}")
def on_report_status(game_ip: int):
    pass