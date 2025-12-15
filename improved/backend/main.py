"""
FastAPI backend - Improved system implementation.
Implements Phase 2 (HTTP/JSON API) and Phase 3 (FastAPI backend).
"""
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Optional, Dict, Any
import uuid
import json
from datetime import datetime

from config import settings
from security import (
    verify_token, create_access_token, create_refresh_token,
    validate_command, sanitize_filename, validate_file_size, validate_command_length,
    get_password_hash, verify_password
)
from data_processor import (
    load_csv, get_dataframe, describe_data, correlation_matrix,
    head_data, tail_data, info_data, generate_plot, clear_session
)
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Python Data Visualization API",
    description="API for data analysis and visualization",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Dependency for authentication (optional for now)
async def get_current_user(token: Optional[str] = None):
    """Get current user from token (optional auth for Phase 4.2)."""
    if not token:
        return None  # Allow anonymous access for now
    try:
        payload = verify_token(token)
        return payload
    except:
        return None


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)


manager = ConnectionManager()


# Request models
class ExecuteCommandRequest(BaseModel):
    command: str
    params: Dict[str, Any]
    session_id: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Python Data Visualization API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/v1/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    request: Request = None  # For rate limiting
):
    """
    Upload CSV dataset (Phase 2.1).
    """
    # Check if filename exists
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Validate filename
    is_valid, result = sanitize_filename(file.filename)
    if not is_valid:
        raise HTTPException(status_code=400, detail=result)
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    is_valid, error = validate_file_size(len(content))
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    # Load CSV
    result = load_csv(content, file.filename, session_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to load CSV"))
    
    return {
        "success": True,
        "session_id": session_id,
        "dataset": result
    }


@app.post("/api/v1/execute")
async def execute_command(
    request_body: ExecuteCommandRequest
):
    """
    Execute whitelisted command (Phase 2.1, Phase 1.1).
    """
    command = request_body.command
    params = request_body.params
    session_id = request_body.session_id
    
    # Validate command length
    is_valid, error = validate_command_length(command)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Validate command
    is_valid, error = validate_command(command, params)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    # Execute command
    if command == "describe":
        result = describe_data(session_id)
    elif command == "corr":
        result = correlation_matrix(session_id)
    elif command == "head":
        n = params.get("n", 5)
        result = head_data(session_id, n)
    elif command == "tail":
        n = params.get("n", 5)
        result = tail_data(session_id, n)
    elif command == "info":
        result = info_data(session_id)
    elif command == "plot":
        result = generate_plot(
            session_id,
            plot_type=params.get("type"),
            x=params.get("x"),
            y=params.get("y"),
            title=params.get("title"),
            xlabel=params.get("xlabel"),
            ylabel=params.get("ylabel"),
            format_type=params.get("format", "plotly")
        )
    else:
        raise HTTPException(status_code=400, detail=f"Command '{command}' not implemented")
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "success": True,
        "command": command,
        "result": result
    }


@app.get("/api/v1/data/describe")
async def get_describe(session_id: str):
    """Get statistical summary."""
    result = describe_data(session_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/api/v1/data/corr")
async def get_corr(session_id: str):
    """Get correlation matrix."""
    result = correlation_matrix(session_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.websocket("/api/v1/ws")
async def websocket_endpoint(websocket: WebSocket, session_id: Optional[str] = None):
    """
    WebSocket endpoint for real-time updates (Phase 2.2).
    """
    if not session_id:
        session_id = str(uuid.uuid4())
    
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)
            
            msg_type = message.get("type")
            
            if msg_type == "PING":
                # Heartbeat
                await manager.send_message(session_id, {
                    "type": "PONG",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            elif msg_type == "COMMAND":
                # Execute command
                command = message.get("command")
                params = message.get("params", {})
                request_id = message.get("request_id", str(uuid.uuid4()))
                
                # Send progress
                await manager.send_message(session_id, {
                    "type": "PROGRESS",
                    "request_id": request_id,
                    "progress": 10,
                    "message": "Processing command..."
                })
                
                # Execute (simplified - in production, use background tasks)
                try:
                    if command == "plot":
                        result = generate_plot(
                            session_id,
                            plot_type=params.get("type"),
                            x=params.get("x"),
                            y=params.get("y"),
                            title=params.get("title"),
                            xlabel=params.get("xlabel"),
                            ylabel=params.get("ylabel")
                        )
                    else:
                        result = {"error": f"Command {command} not supported via WebSocket"}
                    
                    await manager.send_message(session_id, {
                        "type": "RESULT",
                        "request_id": request_id,
                        "result": result
                    })
                except Exception as e:
                    await manager.send_message(session_id, {
                        "type": "ERROR",
                        "request_id": request_id,
                        "error": str(e)
                    })
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

