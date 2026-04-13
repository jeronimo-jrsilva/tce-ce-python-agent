import os
import json
import re
import logging
from typing import List, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.tools import search_knowledge_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_llm():
    base_url = os.getenv("OPENAI_API_BASE")
    api_key = os.getenv("OPENAI_API_KEY", "no-key")
    model_name = os.getenv("LLM_MODEL", "llama3.1")
    
    if not base_url or base_url.strip() == "":
        base_url = None
        logger.info(f"Provedor: OpenAI | Modelo: {model_name}")
    else:
        logger.info(f"Provedor Local: {base_url} | Modelo: {model_name}")

    return ChatOpenAI(
        model=model_name,
        temperature=0,
        openai_api_key=api_key,
        base_url=base_url
    )

async def run_agent(message: str, chat_history: list) -> Tuple[str, List[dict]]:
    greetings = ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]
    if message.lower().strip() in greetings:
        return "Olá! Sou o assistente técnico. Como posso ajudar com dúvidas sobre a base de conhecimento (Composição, Herança, SOLID)?", []

    context = await search_knowledge_base.ainvoke("")
    
    synthesis_prompt = """Você é um assistente técnico especializado do TCE-CE.
Responda APENAS com base no CONTEXTO fornecido.

CONTEXTO:
{context}

REGRAS:
1. Resposta técnica, direta e em Português (UTF-8).
2. Se não estiver no contexto, responda: "Não encontrei informação na base."
3. Sua saída deve ser OBRIGATORIAMENTE um JSON dentro de tags <json></json>.
4. No campo "sources", liste os cabeçalhos das seções utilizadas (ex: "Composição", "Herança").

FORMATO EXIGIDO:
<json>
{{
    "answer": "Sua resposta técnica aqui...",
    "sources": ["Seção 1", "Seção 2"]
}}
</json>
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", synthesis_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    
    chain = prompt | get_llm()
    
    try:
        response = await chain.ainvoke({
            "input": message, 
            "context": context, 
            "chat_history": chat_history
        })
        text = response.content
        logger.info(f"RAW LLM RESPONSE: {text}")
        
        match = re.search(r"<json>(.*?)</json>", text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            # Garante que caracteres de escape não quebrem o JSON
            data = json.loads(json_str)
            return data.get("answer", ""), [{"section": s} for s in data.get("sources", [])]
        
        return text.strip(), []
        
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        return "Erro interno ao processar a resposta.", []
