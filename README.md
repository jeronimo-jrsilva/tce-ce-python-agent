# 🛡️ TCE-CE Python Agent Challenge

Solução robusta para o desafio técnico de Agente de IA com RAG (Retrieval-Augmented Generation), desenvolvida com foco em resiliência, automação e conformidade técnica (Nível A2).

## 🚀 Diferenciais Técnicos

- **Arquitetura de Dois Passos (Research & Synthesis):** Separação clara entre a busca de contexto (Agente) e a formatação da resposta (Sintetizador), garantindo JSON 100% válido.
- **Robustez de Parsing (Tagged Extraction):** Uso de tags XML-Style para extração infalível de dados, eliminando falhas comuns em modelos locais.
- **Agnóstico de Provedor:** Suporte nativo para **Ollama** (Local/GPU) e **OpenAI** (Cloud) via configuração dinâmica.
- **Infraestrutura Automatizada:** Makefile integrado para setup e execução em diferentes ambientes.
- **Deterministic RAG:** Garantia de consulta à Base de Conhecimento em todas as requisições técnicas.

## 🛠️ Stack Tecnológica

- **Backend:** FastAPI (Assíncrono)
- **Orquestração IA:** LangChain
- **Modelos Suportados:** llama3.1 (Ollama), gpt-4o (OpenAI)
- **Infra:** Docker & Docker Compose

## ⚙️ Como Rodar

### 1. Configuração de Ambiente
Copie o arquivo de exemplo e preencha suas variáveis:
```bash
cp .env.example .env
```

### 2. Execução (Docker)
Escolha o seu perfil de execução:

**Perfil Local (Ollama):**
```bash
make run-local
```

**Perfil Cloud (OpenAI):**
```bash
make run-openai
```

A API estará disponível em: `http://localhost:8000`

## 🧪 Testando o Agente

Dispare uma requisição para o endpoint principal:

```bash
curl -X POST http://localhost:8000/messages \
     -H "Content-Type: application/json" \
     -d '{
          "message": "Qual a diferença entre Composição e Herança?",
          "session_id": "minha_sessao_01"
         }'
```

## 📂 Estrutura do Projeto

- `src/main.py`: Endpoint FastAPI e lógica de roteamento.
- `src/agent.py`: Cérebro do Agente (Research & Synthesis).
- `src/tools.py`: Ferramenta de conexão com a Base de Conhecimento externa.
- `Makefile`: Comandos de automação.

---
Desenvolvido por **Jeronimo** (2026).
