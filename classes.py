from typing import List
import asyncio
from dataclasses import dataclass
from fastapi import WebSocket
from utils import create_server
from constants import CREATE_MESSAGE, FETCH_CHANNEL
import json

@dataclass
class User:
    id: str
    username: str
    discriminator: str
    avatar: str
    joined: int
    mail: str
    password: str
    ws: WebSocket

class Server:
    def __init__(self, name) -> None:
        self.clients: List[User] = []
        self.name = name
        self.db = create_server(f"{name}")

    async def broadcast(self, channel: str, user: str, message: str):
        self.db.execute(CREATE_MESSAGE.format(channel, user, message))
        payload = json.dumps({"op": "2", "p": {"user": user, "message": message}})
        if self.clients:
            await asyncio.wait([user.send_text(payload) for user in self.clients])
        self.db.commit()

    def register(self, user: WebSocket):
        self.clients.append(user)

    def disconnect(self, user: WebSocket):
        self.clients.remove(user)
    
    async def fetch(self, channel: str):
        a = self.db.execute(FETCH_CHANNEL.format(channel)).fetchall()
        return [{"id": i[0], "user": i[1], "message": i[2]} for i in a]
