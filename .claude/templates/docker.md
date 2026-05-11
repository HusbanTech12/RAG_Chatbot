# Docker Configuration Template

Use these templates for containerizing the RAG Chatbot application.

## Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim as builder

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

## Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine AS runner

WORKDIR /app

# Set environment
ENV NODE_ENV=production

# Copy necessary files
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Run application
CMD ["node", "server.js"]
```

## Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: rag-backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/rag_chatbot
      - VECTOR_DB_PATH=/data/chroma_db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
      - backend-data:/data
    depends_on:
      - db
    networks:
      - rag-network
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: rag-frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
    networks:
      - rag-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: rag-db
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=rag_chatbot
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - rag-network
    restart: unless-stopped

  # Optional: Vector database (ChromaDB)
  chromadb:
    image: chromadb/chroma:latest
    container_name: rag-chromadb
    ports:
      - "8001:8000"
    volumes:
      - chroma-data:/chroma/chroma
    environment:
      - IS_PERSISTENT=TRUE
    networks:
      - rag-network
    restart: unless-stopped

volumes:
  backend-data:
  postgres-data:
  chroma-data:

networks:
  rag-network:
    driver: bridge
```

## Docker Compose for Development

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: rag-backend-dev
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/rag_chatbot
      - VECTOR_DB_PATH=/data/chroma_db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
      - backend-data:/data
    depends_on:
      - db
    networks:
      - rag-network
    command: fastapi dev main.py --host 0.0.0.0 --port 8000

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: rag-frontend-dev
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    depends_on:
      - backend
    networks:
      - rag-network
    command: npm run dev

  db:
    image: postgres:15-alpine
    container_name: rag-db-dev
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=rag_chatbot
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - rag-network

volumes:
  backend-data:
  postgres-data:

networks:
  rag-network:
    driver: bridge
```

## .dockerignore Files

### Backend .dockerignore
```
# backend/.dockerignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
env/
venv/
.pytest_cache/
.coverage
htmlcov/
*.log
.env
.env.local
*.db
*.sqlite
chroma_db/
```

### Frontend .dockerignore
```
# frontend/.dockerignore
node_modules/
.next/
out/
.env*.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store
*.pem
```

## Usage

### Build and Run with Docker Compose

```bash
# Development
docker-compose -f docker-compose.dev.yml up --build

# Production
docker-compose up --build -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
```

### Build Individual Images

```bash
# Backend
cd backend
docker build -t rag-backend:latest .

# Frontend
cd frontend
docker build -t rag-frontend:latest .
```

### Run Individual Containers

```bash
# Backend
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  rag-backend:latest

# Frontend
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  rag-frontend:latest
```
