# AI API Connector System

A professional, fully functional Agent-Proxy Gateway for connecting external AI agents to internal APIs securely.

## Features

- **Ingestion Pipeline**: Drag-and-drop OpenAPI 3.1 connector onboarding.
- **Vector Database**: Semantic discovery of API functions using ChromaDB.
- **Secure Vault**: Local encrypted storage for API keys and credentials.
- **Stateless Proxy Agent**: Efficient execution of API calls on behalf of external agents.
- **Management Dashboard**: Modern React UI for managing connectors.

## Prerequisites

- Python 3.8+
- Node.js 16+
- Git

## Installation

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Project

### Start Backend

```bash
cd backend
# Ensure venv is active
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Docs: `http://localhost:8000/docs`

### Start Frontend

```bash
cd frontend
npm run dev
```

The Dashboard will be available at `http://localhost:5173`.

## Usage Guide

1. **Upload Connector**: Go to the Dashboard, click "Add Connector", and upload an OpenAPI JSON/YAML file.
2. **Configure Auth**: You will be redirected to enter the required secrets (e.g., API Key).
3. **Agent Query**: External agents can now query the system via `POST /api/v1/agent/query`.

### Example Agent Query

```json
POST http://localhost:8000/api/v1/agent/query
{
  "user_query": "Find customer details for ID 123",
  "conversation_id": "conv-1",
  "user_context_data": {}
}
```

## Architecture

- **Backend**: FastAPI, SQLAlchemy (SQLite), ChromaDB, Local Vault.
- **Frontend**: React, Vite, TailwindCSS.

## Documentation

For detailed information about specific features:

- **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
- **[API Integration](API_INTEGRATION.md)** - How to integrate with the system
- **[LLM Parameter Extraction](LLM_PARAMETER_EXTRACTION.md)** - How parameters are extracted from queries
- **[LLM Function Assessment](LLM_FUNCTION_ASSESSMENT.md)** - How the system selects the right API function
- **[GitHub Publishing](GITHUB_PUBLISHING.md)** - Publishing and deployment guide

