from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.proxy_agent import proxy_agent

router = APIRouter()

class AgentQuery(BaseModel):
    user_query: str
    conversation_id: str
    user_context_data: Optional[Dict[str, Any]] = None

@router.post("/query")
async def agent_query(query: AgentQuery):
    result = await proxy_agent.process_query(query.user_query, query.conversation_id, query.user_context_data)
    return result
