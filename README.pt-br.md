# DocMind: Assistente de Documentação com IA (RAG)

*[Read in English](README.md)*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector--Store-00A896?style=flat-square&logoColor=white)](https://github.com/facebookresearch/faiss)
[![License MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/aj1no/docmind-rag-assistant/ci.yml?branch=main&label=CI&style=flat-square)](https://github.com/aj1no/docmind-rag-assistant/actions)

DocMind Cloud é uma plataforma SaaS fictícia para gerenciamento robusto de documentações internas, criação de índices semânticos e respostas orientadas por Inteligência Artificial. Este repositório implementa o backend de Geração Aumentada de Recuperação (RAG) que alimenta o DocMind Cloud.

---

## O Problema

A documentação técnica escala de forma ineficiente. Quando wikis internas ou documentações de desenvolvedores excedem determinado tamanho, as buscas tradicionais por palavras-chave tornam-se um gargalo. Engenheiros e equipes de suporte perdem tempo analisando páginas extensas.

O DocMind resolve isso utilizando embeddings vetoriais para compreender a semântica da consulta, recuperando exatamente o que é relevante e utilizando um LLM para sintetizar uma resposta imediata e estritamente contextualizada.

---

## Inspiração na Stripe

O esquema de documentação localizado em `docs/` é fortemente inspirado na abordagem da Stripe para documentação de API — separado de forma clara por conceitos (Autenticação, Faturamento, Espaços de Trabalho, etc.), enfatizando a clareza, limites estritos e exemplos amigáveis para desenvolvedores. Representa como um SaaS corporativo real lida com documentações voltadas para o usuário.

---

## Arquitetura RAG

1. **Ingestão:** Analisa arquivos Markdown de `docs/`.
2. **Chunking:** Divide o texto em subconjuntos com limites de 400 a 800 tokens, preservando os metadados.
3. **Embeddings:** Utiliza o modelo leve e local `sentence-transformers` (`all-MiniLM-L6-v2`) para converter textos em vetores de alta dimensão.
4. **Armazenamento Vetorial:** Reconstrói um índice `FAISS` local em memória para correspondência instantânea de similaridade semântica.
5. **Geração:** Envia a consulta para a API do Google Vertex AI / AI Studio (`gemini-2.5-flash`). O prompt do sistema é projetado para evitar alucinações, limitando estritamente o LLM aos blocos recuperados e garantindo a citação correta das fontes.

---

## Tecnologias Utilizadas

- **Python:** Linguagem Principal
- **FastAPI / Uvicorn:** Interface REST de alto desempenho
- **FAISS:** Mecanismo de armazenamento vetorial local
- **Sentence-Transformers:** Modelos de embeddings de código aberto
- **SDK do Google Gemini:** Para geração de texto (`gemini-2.5-flash`)
- **HTML/CSS/JS Puro:** Frontend SPA responsivo e personalizado com interface em Glassmorphism.
- **Tiktoken:** Contagem precisa de tokens

---

## Como Executar

1. **Clonar & Configurar o Ambiente:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Ou `venv\Scripts\activate` no Windows
    pip install -r requirements.txt
    ```

2. **Configurar Variáveis:**
    Copie o arquivo `.env.example` para `.env` e insira sua chave de API:
    ```bash
    cp .env.example .env
    # Edite o .env e insira sua GEMINI_API_KEY
    ```

3. **Iniciar o Servidor da API:**
    ```bash
    uvicorn src.main:app --reload
    ```
    O servidor iniciará em `http://localhost:8000`.

---

## Exemplos Reais de Uso

### Passo 1: Ingerir a documentação
Indexe os documentos fornecidos para que o armazenamento vetorial processe os dados.

```bash
curl -X POST http://localhost:8000/ingest
```

### Passo 2: Fazer uma Pergunta
Consulte a pipeline RAG sobre os limites de faturamento do DocMind.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What happens if I downgrade my plan and have too many documents?",
    "top_k": 3
  }'
```

**Resposta Esperada:**
```json
{
  "answer": "If you downgrade from Pro to Developer and your workspace already exceeds the 50 document limit, your API access will be restricted to read-only until you delete the excess data.",
  "sources": [
    {
      "document": "billing.md",
      "chunk": "Note: If you downgrade from Pro to Developer and your workspace already exceeds the 50 document limit, your API access will be restricted to read-only until you delete excess data.",
      "score": 1.09
    }
  ]
}
```
