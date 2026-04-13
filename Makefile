.PHONY: setup run-local run-openai run-gemini test stop clean

setup:
	pip install -r requirements.txt
	cd frontend && npm install

run-local:
	@echo "🚀 Iniciando Agente (API + React) com OLLAMA (Local)..."
	LLM_MODEL=llama3.1 OPENAI_API_BASE=http://localhost:11434/v1 docker compose up -d --build

run-openai:
	@echo "☁️ Iniciando Agente (API + React) com OPENAI (Nuvem)..."
	LLM_MODEL=gpt-4o-mini OPENAI_API_BASE="" docker compose up -d --build

run-gemini:
	@echo "🌟 Iniciando Agente (API + React) com GEMINI (Nuvem/Google)..."
	LLM_MODEL=gemini-flash-latest OPENAI_API_BASE=https://generativelanguage.googleapis.com/v1beta/openai/ docker compose up -d --build

test:
	pytest tests/test_api.py

stop:
	docker compose down

clean:
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf frontend/node_modules
