# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAG Chatbot is a monorepo containing a FastAPI backend and Next.js frontend for a retrieval-augmented generation chatbot application.

## Architecture

- **Backend** (`backend/`): FastAPI application (Python 3.12)
- **Frontend** (`frontend/`): Next.js 16.2.4 with React 19, TypeScript, and Tailwind CSS v4

## Development Commands

### Backend

The backend uses `uv` for dependency management and requires Python 3.12.

```bash
cd backend

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv sync

# Run development server (default: http://localhost:8000)
fastapi dev main.py

# Run production server
fastapi run main.py
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server (default: http://localhost:3000)
npm run dev

# Build for production
npm run build

# Run production server
npm start

# Lint
npm run lint
```

## Important Notes

### Next.js Version Warning

This project uses Next.js 16.2.4, which has breaking changes from earlier versions. APIs, conventions, and file structure may differ from training data. Check `node_modules/next/dist/docs/` for current documentation before making changes.

### Frontend Configuration

- **Path Alias**: `@/*` maps to the frontend root directory
- **App Router**: Uses Next.js App Router (not Pages Router)
- **TypeScript**: Strict mode enabled
- **Styling**: Tailwind CSS v4 with PostCSS

### Backend Configuration

- **Python Version**: 3.12 (specified in `.python-version`)
- **Package Manager**: Uses `uv` (not pip or poetry)
- **Environment**: `.env` file in backend directory for configuration
