"""WebSocket endpoint for execution progress updates."""

import asyncio
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from redis.asyncio import Redis

from app.dependencies import get_redis
from app.schemas import ExecutionProgress

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for execution updates."""

    def __init__(self):
        # execution_id -> list of websockets
        self.connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, execution_id: str):
        """Accept and store WebSocket connection."""
        await websocket.accept()
        if execution_id not in self.connections:
            self.connections[execution_id] = []
        self.connections[execution_id].append(websocket)

    def disconnect(self, websocket: WebSocket, execution_id: str):
        """Remove WebSocket connection."""
        if execution_id in self.connections:
            self.connections[execution_id].remove(websocket)
            if not self.connections[execution_id]:
                del self.connections[execution_id]

    async def broadcast(self, execution_id: str, message: dict):
        """Broadcast message to all connections for an execution."""
        if execution_id in self.connections:
            for websocket in self.connections[execution_id]:
                try:
                    await websocket.send_json(message)
                except Exception:
                    pass  # Connection might be closed


manager = ConnectionManager()


@router.websocket("/ws/executions/{execution_id}")
async def execution_progress(
    websocket: WebSocket,
    execution_id: UUID,
):
    """WebSocket endpoint for execution progress updates.

    Connect to receive real-time updates about task execution.

    Events:
    - {"type": "status", "data": {"status": "running", "subtask": "..."}}
    - {"type": "log", "data": {"message": "...", "level": "info"}}
    - {"type": "complete", "data": {"status": "completed", "results": {...}}}
    - {"type": "error", "data": {"error": "..."}}
    """
    execution_id_str = str(execution_id)

    await manager.connect(websocket, execution_id_str)

    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connected",
            "data": {"execution_id": execution_id_str},
        })

        # Keep connection alive and wait for messages
        while True:
            try:
                # Wait for any message (ping/pong or close)
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0,
                )
                # Handle ping
                if data == "ping":
                    await websocket.send_text("pong")
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.send_text("ping")

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket, execution_id_str)


async def send_progress_update(execution_id: str, progress: ExecutionProgress):
    """Send progress update to all connected clients.

    Called by ExecutionEngine during task execution.
    """
    await manager.broadcast(execution_id, progress.model_dump())
