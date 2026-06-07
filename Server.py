from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
import threading
import webview

app = FastAPI()

# Твой HTML (оставляем его здесь)
html_layout = """ (ВСТАВЬ СЮДА ВЕСЬ СВОЙ HTML-КОД) """

@app.get("/")
async def get():
    return HTMLResponse(content=html_layout)

# Базовый менеджер соединений
class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    async def connect(self, ws):
        await ws.accept()
        self.active_connections.append(ws)
    def disconnect(self, ws):
        self.active_connections.remove(ws)
    async def broadcast(self, message):
        for conn in self.active_connections:
            await conn.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except:
        manager.disconnect(websocket)

if __name__ == "__main__":
    def run_server():
        # СТАВИМ 0.0.0.0 ЧТОБЫ ТУННЕЛЬ РАБОТАЛ
        uvicorn.run(app, host="0.0.0.0", port=8000)

    threading.Thread(target=run_server, daemon=True).start()

    window = webview.create_window("Video Messenger", "http://127.0.0.1:8000", width=1020, height=720)
    webview.start(private_mode=False)
