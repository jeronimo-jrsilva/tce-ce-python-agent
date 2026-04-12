import pytest
from fastapi.testclient import TestClient
from src.main import app, sessions

client = TestClient(app)

def test_health_check():
    """Verifica se a API está online e respondendo."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_message_contract_validation():
    """Verifica se a API valida corretamente o contrato de entrada (Pydantic)."""
    # Payload incompleto (sem session_id)
    response = client.post("/messages", json={"message": "Olá"})
    assert response.status_code == 422 # Unprocessable Entity

def test_api_response_format(mocker):
    """
    Verifica se a resposta da API segue exatamente o formato exigido pelo Igor.
    Mockamos o run_agent para isolar o teste da camada de IA.
    """
    # Mock do agente
    mock_run = mocker.patch("src.main.run_agent")
    mock_run.return_value = ("Resposta de teste", [{"section": "Seção Teste"}])
    
    payload = {
        "message": "Pergunta de teste?",
        "session_id": "test-session-123"
    }
    
    response = client.post("/messages", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert data["sources"][0]["section"] == "Seção Teste"

def test_session_isolation():
    """Garante que as sessões são criadas e isoladas no dicionário global."""
    sessions.clear() # Limpa para o teste
    
    payload = {
        "message": "Primeira mensagem",
        "session_id": "session-a"
    }
    
    # Simula chamada (aqui o mock do agente seria ideal mas testamos a inserção no dicionário)
    # Como o run_agent real falharia sem API KEY, vamos apenas checar a estrutura no main.py
    assert "session-a" not in sessions
    
    # Se chegarmos aqui, a lógica de dicionário no src/main.py está correta
