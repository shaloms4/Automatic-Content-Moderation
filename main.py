from fastapi import FastAPI
from pydantic import BaseModel
from detector import hybrid_moderate
from database import ModerationDatabase
from typing import Dict, Optional

app = FastAPI(
    title="CogMod API",
    description="Cognitive Science Project - Hybrid Content Moderation (Memory + Attention)",
    version="1.0"
)

# Initialize Database
db = ModerationDatabase()

class TextInput(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    original_text: str
    moderated_text: str
    toxicity_score: float
    is_toxic: bool
    raw_model_score: float
    method: str
    flagged_words: Optional[list] = None


@app.get("/")
def home():
    return {
        "message": "🧠 CogMod Cognitive Content Moderation API is running",
        "features": ["Semantic Memory (Rule-based)", "Transformer Attention (BERT)", "Hybrid Reasoning", "Logging"],
        "status": "healthy"
    }


@app.post("/moderate", response_model=ModerationResponse)
def moderate_text(input: TextInput):
    """Main endpoint for content moderation"""
    # Get moderation result
    result = hybrid_moderate(input.text)
    
    # Log to database
    db.log_moderation(result)
    
    # Prepare response
    response = {
        "original_text": result["original_text"],
        "moderated_text": result["moderated_text"],
        "toxicity_score": result["toxicity_score"],
        "is_toxic": result["is_toxic"],
        "raw_model_score": result.get("raw_model_score", 0.0),
        "method": result["method"],
        "flagged_words": result["rule_based"].get("flagged_words", [])
    }
    
    return response


@app.get("/history")
def get_moderation_history(limit: int = 20):
    """Get recent moderation logs"""
    history = db.get_history(limit)
    return {"history": history, "count": len(history)}


@app.get("/stats")
def get_system_stats():
    """Get moderation statistics"""
    stats = db.get_stats()
    return stats


@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected"}


# Run directly for testing
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting CogMod API with Database Logging...")
    uvicorn.run(app, host="127.0.0.1", port=8000)