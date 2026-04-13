# 🛡️ TCE-CE Agente de IA Técnico (Python Agent Challenge)

Este repositório contém uma solução completa para o desafio técnico do TCE-CE: um assistente virtual inteligente capaz de realizar **RAG (Retrieval-Augmented Generation)** sobre uma base de conhecimento técnica externa em tempo real.

---

## 🚀 Guia de Início Rápido (Multi-Provedor)

A solução foi projetada para ser agnóstica ao modelo de linguagem, permitindo execução local ou em nuvem via **Docker Compose**.

### 📋 Pré-requisitos
- Docker e Docker Compose instalados.
- Se for rodar localmente: **Ollama** rodando no host.

### 1️⃣ Cenário A: Execução Local (Ollama)
Ideal para desenvolvimento offline e sem custos. Utiliza o modelo **Llama 3.1**.
1. Certifique-se que o Ollama está rodando e o modelo baixado (`ollama pull llama3.1`).
2. Execute: `make run-local`
3. Acesse: **[http://localhost:5173](http://localhost:5173)**

### 2️⃣ Cenário B: Execução Google Cloud (Gemini) - TESTADO
Ideal para performance rápida usando o nível gratuito do Google AI Studio.
1. Edite o `.env` com sua `OPENAI_API_KEY` (Chave do Gemini) e garanta que `OPENAI_API_BASE` aponta para o endpoint do Google.
2. Execute: `make run-gemini`
3. Acesse: **[http://localhost:5173](http://localhost:5173)**

### 3️⃣ Cenário C: Execução OpenAI (GPT-4o)
Cenário padrão para produção e precisão máxima.
1. Edite o `.env` com sua chave da OpenAI e limpe o campo `OPENAI_API_BASE`.
2. Execute: `make run-openai`
3. Acesse: **[http://localhost:5173](http://localhost:5173)**

---

## 🏗️ Arquitetura e Diferenciais (Nível A2)

O projeto implementa padrões de engenharia avançados, superando a base consistente do nível A1:

- **Orquestração Desacoplada:** Separação clara entre API (FastAPI), Orquestrador (LangChain) e Ferramentas (Tools).
- **Gestão de Sessão:** Uso de `session_id` para manter histórico de conversa (até 10 interações), permitindo perguntas de acompanhamento.
- **Frontend Reativo:** Interface profissional em React/Vite com Dark Mode, renderização de Markdown e visualização de fontes.
- **Robustez de Parsing:** Extração de dados via XML Tags para garantir integridade do JSON mesmo em modelos menores.
- **Fidelidade (Grounding):** O agente é instruído a não alucinar e responder apenas com base na KB fornecida.

---

## 🧭 Endpoints e Ferramentas

| Recurso | URL | Descrição |
| :--- | :--- | :--- |
| **Interface de Produção** | `http://localhost:5173` | UI Completa (React/Vite) |
| **Lab de Debug** | `http://localhost:8000/debug` | Interface minimalista para validação de backend |
| **API Docs (Swagger)** | `http://localhost:8000/docs` | Documentação técnica automática |

---

## 🧪 Sugestões de Testes Manuais (Demonstração)

1. **Especialidade:** "O que a base diz sobre Herança?" (Deve listar a seção "Herança").
2. **Nuance:** "É correto colocar lógica no endpoint?" (Deve citar a exceção para projetos pequenos).
3. **Fallback:** "Como configuro o banco de dados?" (Deve responder que não encontrou a informação).
4. **Memória:** Pergunte algo, depois diga: "Pode resumir isso?" (O agente usará o histórico da sessão).

---
**Desenvolvido para o Desafio TCE-CE 2026.**
