from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from ..services.summarize import summarize_text
from ..services.fetch import fetch_webpage_content
from ..models.schemas import SummaryRequest, SummaryResponse, SummaryType
from ..config import get_settings
import json

router = APIRouter()
settings = get_settings()

@router.post("/summarize")
async def create_summary(request: SummaryRequest):
    try:
        if request.type == SummaryType.URL:
            content = await fetch_webpage_content(request.content)
        else:
            content = request.content
            
        summary = await summarize_text(content, request.max_length)
        return SummaryResponse(summary=summary)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to generate summary: {str(e)}"}
        )

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            request = SummaryRequest(**json.loads(data))
            
            if request.type == SummaryType.URL:
                content = await fetch_webpage_content(request.content)
            else:
                content = request.content
                
            summary = await summarize_text(content, request.max_length)
            await websocket.send_text(json.dumps({"summary": summary}))
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.close(code=1011, reason=str(e))
