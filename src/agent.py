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
    # Detecta se deve usar Ollama (Local) ou OpenAI (Nuvem)
    base_url = os.getenv("OPENAI_API_BASE")
    api_key = os.getenv("OPENAI_API_KEY", "no-key")
    model_name = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    # Se base_url for uma string vazia ou None no .env, o LangChain usa o padrão OpenAI
    if not base_url or base_url.strip() == "":
        base_url = None
        logger.info(f"Usando Provedor: OpenAI | Modelo: {model_name}")
    else:
        logger.info(f"Usando Provedor Local: {base_url} | Modelo: {model_name}")

    return ChatOpenAI(
        model=model_name,
        temperature=0,
        openai_api_key=api_key,
        base_url=base_url
    )

async def run_agent(message: str, chat_history: list) -> Tuple[str, List[dict]]:
    # 1. Busca Determinística (Sempre consulta a base técnica)
    greetings = ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]
    if message.lower().strip() in greetings:
        return "Olá! Sou o assistente técnico. Como posso ajudar com dúvidas sobre a base de conhecimento (Composição, Herança, SOLID)?", []

    context = await search_knowledge_base.ainvoke("")
    
    # 2. Síntese com Instrução de Formato Rígida (XML Tags)
    synthesis_prompt = """
    Você é um assistente técnico especializado.
    Sua única fonte de verdade é o CONTEXTO fornecido abaixo.
    
    CONTEXTO:
    {context}
    
    REGRAS:
    - Responda de forma direta e técnica (máximo 3 parágrafos).
    - Se a informação não estiver na base, responda: "Não encontrei informação na base."
    - Sua saída deve ser OBRIGATORIAMENTE um JSON dentro de tags <json></json>.
    
    FORMATO EXIGIDO:
    <json>
    {{
        "answer": "Sua resposta técnica aqui...",
        "sources": ["Nome da Seção 1", "Nome da Seção 2"]
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
        
        # 3. Parsing Robusto via Tags (Independente do modelo)
        match = re.search(r"<json>(.*?)</json>", text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            data = json.loads(json_str)
            return data.get("answer", ""), [{"section": s} for s in data.get("sources", [])]
        
        # Fallback se o LLM não usou as tags (comum em modelos GPT-3.5)
        return text.strip(), []
        
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        return "Erro interno ao processar a resposta.", []

