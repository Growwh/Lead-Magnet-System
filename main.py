from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.agent import LeadMagnetAgent
from pathlib import Path

app = FastAPI()
agent = LeadMagnetAgent()

class RepurposeRequest(BaseModel):
    input_source: str
    brand_context: str
    voice_context: str

@app.post("/generate")
async def generate_lead_magnet(request: RepurposeRequest):
    # Inject dynamic context into the agent
    # You would modify agent.py to accept these strings instead of reading files
    try:
        result = await agent.run(
            user_input=request.input_source,
            # Pass these to a modified build_system_prompt
            brand_text=request.brand_context,
            voice_text=request.voice_context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
