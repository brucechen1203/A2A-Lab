from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent_card import AGENT_CARD
from handlers import handle_task

app = FastAPI(title="Echo A2A Agent")


# Endpoint 1: Agent Card
@app.get("/.well-known/agent.json")
async def get_agent_card():
	return AGENT_CARD


@app.get("/health")
async def health():
	return {"status": "ok", "agent": AGENT_CARD["id"]}


# Pydantic models for the A2A task message schema
class TextPart(BaseModel):
	type: str = "text"
	text: str


class Message(BaseModel):
	role: str
	parts: list[TextPart]


class TaskRequest(BaseModel):
	id: str
	sessionId: Optional[str] = None
	message: Message
	metadata: Optional[dict[str, Any]] = None


# Endpoint 2: Send Task
@app.post("/tasks/send")
async def send_task(request: TaskRequest):
	if not request.message.parts:
		raise HTTPException(status_code=400, detail="message.parts must not be empty")

	result_text = await handle_task(request)
	return {
		"id": request.id,
		"status": {"state": "completed"},
		"artifacts": [
			{
				"parts": [{"type": "text", "text": result_text}],
			}
		],
	}
