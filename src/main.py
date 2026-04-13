import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict
from src.agent import run_agent

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TCE-CE Agent Challenge",
    description="Backend para assistente virtual baseado em IA com RAG em KB externa."
)

# Repositório de sessões em memória (Em prod: Usar Redis)
# Estrutura: { "session_id": [HumanMessage, AIMessage, ...] }
sessions: Dict[str, List] = {}

class Source(BaseModel):
    section: str

class MessageRequest(BaseModel):
    message: str
    session_id: str

class MessageResponse(BaseModel):
    answer: str
    sources: List[Source]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/debug", response_class=HTMLResponse)
async def debug_page():
    with open("src/static/debug.html", "r") as f:
        return f.read()

@app.post("/messages", response_model=MessageResponse)
async def chat(request: MessageRequest):
    logger.info(f"Recebendo mensagem para sessão: {request.session_id}")
    
    try:
        # Recupera ou inicializa o histórico da sessão
        history = sessions.get(request.session_id, [])
        
        # Executa o agente (passando a mensagem e o histórico atual)
        answer, sources = await run_agent(request.message, history)
        
        # Atualiza o histórico (Opcional: Limitar tamanho para economizar tokens)
        # Por simplicidade, adicionamos Human e AI message ao histórico
        # Em LangChain real, usaríamos ChatMessageHistory
        history.append(("human", request.message))
        history.append(("ai", answer))
        sessions[request.session_id] = history[-10:] # Mantém as últimas 10 interações
        
        return MessageResponse(
            answer=answer,
            sources=sources
        )
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a requisição.")

@app.get("/health")
async def health():
    return {"status": "healthy", "sessions_active": len(sessions)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
