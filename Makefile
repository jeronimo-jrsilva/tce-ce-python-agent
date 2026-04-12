.PHONY: setup run-local run-openai test stop clean

setup:
	pip install -r requirements.txt

run-local:
	@echo "🚀 Iniciando Agente com OLLAMA (Local)..."
	LLM_MODEL=llama3.1 OPENAI_API_BASE=http://localhost:11434/v1 docker compose up -d --build

run-openai:
	@echo "☁️ Iniciando Agente com OPENAI (Nuvem)..."
	LLM_MODEL=gpt-4o OPENAI_API_BASE="" docker compose up -d --build

test:
	pytest tests/test_api.py

stop:
	docker compose down

clean:
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +
