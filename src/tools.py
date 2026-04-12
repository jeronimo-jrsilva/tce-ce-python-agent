import httpx
import os
from langchain.tools import tool
from typing import List, Dict

@tool
async def search_knowledge_base(query: str) -> str:
    """
    Busca informações na Base de Conhecimento oficial do TCE-CE via HTTP.
    Deve ser usada sempre que o usuário fizer perguntas sobre processos, 
    regras, benefícios ou informações técnicas do órgão.
    """
    kb_url = os.getenv("KB_URL")
    if not kb_url:
        return "Erro: URL da Base de Conhecimento não configurada."

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(kb_url)
            response.raise_for_status()
            content = response.text
            
            # Por enquanto, retornamos o conteúdo integral. 
            # Em versões futuras, podemos implementar busca semântica ou regex por query.
            return content
    except Exception as e:
        return f"Erro ao acessar a Base de Conhecimento: {str(e)}"

def extract_sections(markdown_content: str) -> List[str]:
    """
    Extrai os nomes das seções (headers) de um texto Markdown.
    Utilizado para preencher o campo 'sources'.
    """
    sections = []
    for line in markdown_content.split("\n"):
        if line.startswith("#"):
            # Remove os '#' e espaços extras
            sections.append(line.lstrip("#").strip())
    return sections
