# RAG Chatbot - Quick Start Guide

## Issues Fixed ✓

### 1. Backend Migration Complete
- ✓ Migrated from deprecated `google.generativeai` to `google.genai`
- ✓ Fixed model 404 errors
- ✓ Updated to supported models: `gemini-2.5-flash` and `gemini-embedding-2`

### 2. Knowledge Base Issue Resolved
- **Problem:** Chatbot was responding "I cannot answer your question as the provided context does not contain any relevant information"
- **Cause:** ChromaDB vector database was empty (0 documents)
- **Solution:** Added sample document and verified retrieval works

## How to Add Documents to Your Chatbot

### Method 1: Using the API (Recommended)

```bash
# Upload a text file
curl -X POST "http://localhost:8001/api/v1/documents/upload" \
  -F "file=@your_document.txt"

# Upload a PDF (basic support)
curl -X POST "http://localhost:8001/api/v1/documents/upload" \
  -F "file=@your_document.pdf"
```

### Method 2: Using Python

```python
import requests

url = "http://localhost:8001/api/v1/documents/upload"
files = {'file': open('your_document.txt', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

### Method 3: Using the Frontend

Your Next.js frontend should have a document upload interface. If not, you can add one.

## Supported File Types

Currently supported:
- `.txt` - Plain text files
- `.pdf` - PDF files (basic text extraction)

## How It Works

1. **Upload:** Document is uploaded via API
2. **Chunking:** Text is split into chunks (default: 1000 chars with 200 overlap)
3. **Embedding:** Each chunk is converted to a vector using `gemini-embedding-2`
4. **Storage:** Vectors are stored in ChromaDB
5. **Retrieval:** When you ask a question, relevant chunks are retrieved
6. **Generation:** Gemini generates an answer based on retrieved context

## Testing Your Knowledge Base

```bash
# Check how many documents are in the database
curl http://localhost:8001/api/v1/documents

# Test a chat query
curl -X POST "http://localhost:8001/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here"}'
```

## Current Status

✓ Backend running on port 8001
✓ 2 document chunks in ChromaDB
✓ Chatbot successfully answering questions
✓ No deprecation warnings
✓ No model errors

## Next Steps

1. **Add Your Own Documents:** Upload documents relevant to your use case
2. **Test the Frontend:** Make sure your Next.js app connects to the backend
3. **Monitor Performance:** Check response quality and adjust chunk size if needed
4. **Add More File Types:** Extend support for DOCX, Markdown, etc. if needed

## Troubleshooting

**If chatbot says "no relevant information":**
- Check if documents are uploaded: `curl http://localhost:8001/api/v1/documents`
- Verify ChromaDB has documents (see Python script below)

**Check ChromaDB contents:**
```python
import chromadb
client = chromadb.PersistentClient(path='./storage/chroma_db')
collections = client.list_collections()
for col in collections:
    print(f'{col.name}: {col.count()} documents')
```

## API Endpoints

- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents` - List uploaded documents
- `DELETE /api/v1/documents/{id}` - Delete document
- `POST /api/v1/chat` - Chat with the bot
- `GET /api/v1/conversations` - List conversations
- `GET /health` - Health check
