# Quick Start Guide

This guide will help you get the RAG Chatbot project up and running quickly.

## Prerequisites

- Python 3.12
- Node.js 18+ and npm
- Git

## Initial Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd RAG_Chatbot
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment (if not exists)
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies with uv
pip install uv
uv sync

# Create .env file
cp .env.example .env  # If example exists
# or create manually with required variables

# Run development server
fastapi dev main.py
```

Backend will be available at http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at http://localhost:3000

## Environment Variables

### Backend (.env)

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=sqlite:///./app.db

# Vector Database
VECTOR_DB_PATH=./chroma_db

# JWT Secret
JWT_SECRET=your_secret_key_here

# Environment
ENVIRONMENT=development
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Verify Installation

### Backend

```bash
cd backend
curl http://localhost:8000
# Should return: {"Hello": "World"}
```

### Frontend

Open http://localhost:3000 in your browser. You should see the Next.js welcome page.

## Next Steps

1. **Implement RAG functionality**: Use the `rag-architect` agent
2. **Build chat UI**: Use the `frontend-dev` agent
3. **Connect frontend to backend**: Use the `fullstack-integrator` agent
4. **Add tests**: Use the `test-engineer` agent
5. **Deploy**: Use the `devops-engineer` agent

## Common Issues

### Backend won't start

- Check Python version: `python --version` (should be 3.12)
- Ensure virtual environment is activated
- Check if port 8000 is already in use

### Frontend won't start

- Check Node version: `node --version` (should be 18+)
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Check if port 3000 is already in use

### CORS errors

- Ensure backend CORS middleware is configured to allow http://localhost:3000
- Check that API URL in frontend matches backend URL

## Development Workflow

1. Start backend: `cd backend && fastapi dev main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Make changes
4. Test changes
5. Commit with descriptive messages
6. Push to repository

## Getting Help

- Check CLAUDE.md for project documentation
- Use specialized agents in `.claude/agents/` for specific tasks
- Review templates in `.claude/templates/` for code patterns
- Read `.claude/README.md` for agent documentation
