# Testing Template

Use these templates for writing tests in the RAG Chatbot project.

## Backend Tests (pytest)

### Test API Endpoints

```python
# backend/tests/test_api.py
import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World"}

@pytest.mark.asyncio
async def test_create_resource(client: AsyncClient):
    """Test resource creation."""
    payload = {
        "name": "Test Resource",
        "description": "Test description"
    }
    response = await client.post("/api/v1/resources", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data

@pytest.mark.asyncio
async def test_create_resource_validation_error(client: AsyncClient):
    """Test resource creation with invalid data."""
    payload = {}  # Missing required fields
    response = await client.post("/api/v1/resources", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
```

### Test RAG Pipeline

```python
# backend/tests/test_rag.py
import pytest
from unittest.mock import Mock, AsyncMock, patch

@pytest.mark.asyncio
async def test_document_chunking():
    """Test document chunking."""
    from backend.rag.ingestion import DocumentChunker
    
    chunker = DocumentChunker(chunk_size=100, chunk_overlap=20)
    text = "A" * 250
    chunks = chunker.chunk_text(text)
    
    assert len(chunks) > 1
    assert all(len(chunk['text']) <= 100 for chunk in chunks)

@pytest.mark.asyncio
async def test_embedding_generation():
    """Test embedding generation with mocked API."""
    from backend.rag.embeddings import EmbeddingModel
    
    with patch('openai.AsyncOpenAI') as mock_client:
        # Mock the API response
        mock_response = Mock()
        mock_response.data = [Mock(embedding=[0.1] * 1536)]
        mock_client.return_value.embeddings.create = AsyncMock(return_value=mock_response)
        
        model = EmbeddingModel()
        embedding = await model.embed("test text")
        
        assert len(embedding) == 1536
        assert all(isinstance(x, float) for x in embedding)

@pytest.mark.asyncio
async def test_retrieval():
    """Test document retrieval."""
    from backend.rag.retrieval import Retriever
    
    # Mock dependencies
    mock_vector_store = Mock()
    mock_vector_store.search = AsyncMock(return_value={
        'documents': [['doc1', 'doc2']],
        'metadatas': [[{'source': 'test1'}, {'source': 'test2'}]],
        'distances': [[0.1, 0.2]],
        'ids': [['id1', 'id2']]
    })
    
    mock_embedding_model = Mock()
    mock_embedding_model.embed = AsyncMock(return_value=[0.1] * 1536)
    
    retriever = Retriever(mock_vector_store, mock_embedding_model)
    results = await retriever.retrieve("test query", n_results=2)
    
    assert len(results) == 2
    assert results[0]['text'] == 'doc1'
    assert results[0]['distance'] == 0.1
```

### Test Fixtures

```python
# backend/tests/conftest.py
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.main import app

@pytest.fixture
async def client():
    """Async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def db_session():
    """Database session for testing."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client."""
    with patch('openai.AsyncOpenAI') as mock:
        yield mock
```

## Frontend Tests (Jest + React Testing Library)

### Component Tests

```typescript
// frontend/__tests__/components/ChatMessage.test.tsx
import { render, screen } from '@testing-library/react';
import ChatMessage from '@/app/components/ChatMessage';

describe('ChatMessage', () => {
  it('renders user message correctly', () => {
    render(
      <ChatMessage
        role="user"
        content="Hello, world!"
        timestamp={new Date('2024-01-01T12:00:00')}
      />
    );

    expect(screen.getByText('Hello, world!')).toBeInTheDocument();
  });

  it('renders assistant message correctly', () => {
    render(
      <ChatMessage
        role="assistant"
        content="Hi there!"
      />
    );

    expect(screen.getByText('Hi there!')).toBeInTheDocument();
  });

  it('applies correct styling for user messages', () => {
    const { container } = render(
      <ChatMessage role="user" content="Test" />
    );

    const messageDiv = container.querySelector('.bg-blue-500');
    expect(messageDiv).toBeInTheDocument();
  });
});
```

### API Integration Tests

```typescript
// frontend/__tests__/api/chat.test.ts
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.post('http://localhost:8000/api/v1/chat', (req, res, ctx) => {
    return res(ctx.json({ response: 'Test response' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Chat API', () => {
  it('sends message and receives response', async () => {
    const response = await fetch('http://localhost:8000/api/v1/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: 'Hello' }),
    });

    const data = await response.json();
    expect(data.response).toBe('Test response');
  });

  it('handles API errors', async () => {
    server.use(
      rest.post('http://localhost:8000/api/v1/chat', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ error: 'Server error' }));
      })
    );

    const response = await fetch('http://localhost:8000/api/v1/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: 'Hello' }),
    });

    expect(response.status).toBe(500);
  });
});
```

### Jest Configuration

```javascript
// frontend/jest.config.js
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
  collectCoverageFrom: [
    'app/**/*.{js,jsx,ts,tsx}',
    '!app/**/*.d.ts',
    '!app/**/*.stories.{js,jsx,ts,tsx}',
  ],
};

module.exports = createJestConfig(customJestConfig);
```

```javascript
// frontend/jest.setup.js
import '@testing-library/jest-dom';
```

## Running Tests

### Backend
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_read_root

# Run with verbose output
pytest -v

# Run only failed tests
pytest --lf
```

### Frontend
```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch

# Run specific test file
npm test -- ChatMessage.test.tsx
```
