from typing import List
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
import json
import asyncio
from constants import *
from classes import *
from utils import *

from starlette.websockets import WebSocketDisconnect

"""
    Prerequisites
"""

users = create_db("users.db")
users.execute(CREATE_USERS_TABLE)
users.commit()


servers = {"global": Server("global")}

app = FastAPI()

"""
    REST API
"""

@app.get("/")
async def main():
    return HTMLResponse(HTML)

@app.get("/fetch/{server}/{channel}")
async def fetch(server: str, channel: str):
    data = await servers[server].fetch(channel)
    return JSONResponse(data)

"""
    Websocket
"""

@app.websocket("/ws/{server}/{channel}")
async def ws_main(ws: WebSocket, server: str, channel: str):
    await ws.accept()
    servers[server].register(ws)
    try:
        while True:
            data = await ws.receive_text()
            await servers[server].broadcast(channel, "User", f"{data}")
    except WebSocketDisconnect:
        servers[server].disconnect(ws)