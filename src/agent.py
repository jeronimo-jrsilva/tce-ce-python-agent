import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.tools import search_knowledge_base

SYSTEM_PROMPT = """
Você é um assistente virtual especializado em informações do TCE-CE (Tribunal de Contas do Estado do Ceará).

REGRAS SOBERANAS:
1. Use SEMPRE a ferramenta 'search_knowledge_base' para buscar informações antes de responder qualquer pergunta técnica.
2. Baseie sua resposta EXCLUSIVAMENTE nas informações retornadas pela ferramenta.
3. Se a informação não estiver na base de conhecimento ou se a ferramenta retornar um erro, responda exatamente: "Não encontrei informação suficiente para responder a sua pergunta na Base de Conhecimento."
4. No final da sua resposta, você deve listar os títulos das seções consultadas no seguinte formato: "FONTES: Seção 1, Seção 2".
5. Mantenha um tom profissional e prestativo.
"""

def get_agent_executor():
    # Suporte a provedores customizados (ex: Ollama) via variável de ambiente
    base_url = os.getenv("OPENAI_API_BASE")
    
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY", "no-key"),
        base_url=base_url # Se None, usa o padrão da OpenAI
    )
    
    tools = [search_knowledge_base]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

async def run_agent(message: str, chat_history: list):
    executor = get_agent_executor()
    
    response = await executor.ainvoke({
        "input": message,
        "chat_history": chat_history
    })
    
    full_answer = response["output"]
    
    sources = []
    if "FONTES:" in full_answer:
        parts = full_answer.split("FONTES:")
        answer = parts[0].strip()
        raw_sources = parts[1].strip().split(",")
        sources = [{"section": s.strip()} for s in raw_sources if s.strip()]
    else:
        answer = full_answer
        
    return answer, sources
