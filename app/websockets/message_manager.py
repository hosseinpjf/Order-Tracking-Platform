from typing import Dict
from fastapi import WebSocket

class MessageConnectionManager:
    def __init__(self):
        # Maintaining active connections: By user and device 
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        # user_id → { device_id → websocket }

    # ----------------------------<< Establish Connection >>----------------------------
    async def connect(self, user_id: str, device_id: str, websocket: WebSocket):
        # 1) Accepting WebSocket connection
        await websocket.accept()

        # 2) If the user is connecting for the first time → Creating an empty dict
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}

        # 3) Closing the old connection
        old_ws = self.active_connections[user_id].get(device_id)
        if old_ws is not None:
            try:
                await old_ws.close()
            except Exception:
                pass

        # 4) Creating a new connection for this device_id
        self.active_connections[user_id][device_id] = websocket

    # ----------------------------<< Disconnect >>----------------------------
    async def disconnect(self, user_id: str, device_id: str):
        user_connections = self.active_connections.get(user_id)

        # 1) Checking for user existence (In the active connections dictionary)
        if user_connections is None: return

        # 2) Remove WebSocket
        ws = user_connections.pop(device_id, None)

        if ws is not None:
            try:
                # 3) Connection truly closed
                await ws.close()
            except Exception:
                # If it had already been closed (no problem)
                pass

        # 4) Delete User (If no device is connected)
        if not user_connections:
            self.active_connections.pop(user_id)

    # ----------------------------<< Send Message to a User (all devices) >>----------------------------
    async def send_to_user(self, user_id: str, data: dict) -> bool:
        user_connections = self.active_connections.get(user_id)

        # 1) If the user does not have an active connection → Don't do anything
        if user_connections is None: return False

        dead_devices: list[str] = []
        sent_to_at_least_one = False

        # 2) Copying from the devices → To prevent errors during execution
        devices_snapshot = list(user_connections.items())

        # 3) Send a message to all of this user's online devices
        for device_id, ws in devices_snapshot:
            try:
                await ws.send_json(data)
                sent_to_at_least_one = True
            except Exception:
                # Device is unavailable (Connection lost / Broken)
                dead_devices.append(device_id)

        # 4) Clearing out inoperative devices
        for device_id in dead_devices:
            await self.disconnect(user_id, device_id)

        return sent_to_at_least_one

    # ----------------------------<< Check if a user has any active device >>----------------------------
    def is_online(self, user_id: str) -> bool:
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0