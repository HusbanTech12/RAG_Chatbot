# 🎉 RAG Chatbot with FREE Hugging Face Models

## ✅ Migration Complete

Your RAG chatbot now uses **completely free** Hugging Face models instead of paid APIs!

## 🆓 What's Free

- **LLM**: Mistral-7B-Instruct-v0.2 (text generation)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (768 dimensions)
- **API**: Hugging Face Inference API (free tier)

## 🚀 Quick Start

### Step 1: Get Your FREE API Key

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name (e.g., "RAG Chatbot")
4. Select "Read" access
5. Click "Generate token"
6. Copy your token

### Step 2: Update Configuration

Edit `backend/.env` and replace the placeholder:

```env
HF_API_KEY=your_actual_token_here
```

### Step 3: Restart Backend

```bash
cd /mnt/d/Projects/RAG_Chatbot/backend
pkill -f "fastapi dev main.py"
.venv/bin/fastapi dev main.py --host 0.0.0.0 --port 8001
```

### Step 4: Test the System

#### Upload a Test Document

```bash
cat > /tmp/test_doc.txt << 'EOF'
Hugging Face is a platform for machine learning and AI.
It provides free access to thousands of pre-trained models.
The Inference API allows you to use these models without hosting them yourself.
Mistral-7B is a powerful open-source language model.
EOF

curl -X POST -F "file=@/tmp/test_doc.txt" http://localhost:8001/api/v1/documents/upload
```

#### Test Chat

```bash
curl -X POST "http://localhost:8001/api/v1/chat?query=What+is+Hugging+Face?"
```

Or open http://localhost:3000 in your browser and start chatting!

## 📊 System Architecture

```
User Query
    ↓
Document Upload → Chunking → HF Embeddings → ChromaDB
    ↓
Query → HF Embeddings → Vector Search → Retrieved Docs
    ↓
Retrieved Docs + Query → Mistral-7B → Streaming Response
```

## 🔧 Configuration

### Current Models

**Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- 768-dimensional embeddings
- Fast and efficient
- Great for semantic search

**LLM Model**: `mistralai/Mistral-7B-Instruct-v0.2`
- 7 billion parameters
- Instruction-tuned
- Good balance of speed and quality

### Alternative Free Models

You can change models in `backend/.env`:

**For Embeddings:**
```env
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2  # Better quality, slower
EMBEDDING_MODEL=sentence-transformers/paraphrase-MiniLM-L3-v2  # Faster, smaller
```

**For LLM:**
```env
LLM_MODEL=meta-llama/Llama-2-7b-chat-hf  # Llama 2
LLM_MODEL=google/flan-t5-large  # Smaller, faster
LLM_MODEL=tiiuae/falcon-7b-instruct  # Falcon
```

## 🎯 API Endpoints

### Health Check
```bash
GET http://localhost:8001/health
```

### Upload Document
```bash
POST http://localhost:8001/api/v1/documents/upload
Content-Type: multipart/form-data
Body: file=@document.txt
```

### Chat (Streaming)
```bash
POST http://localhost:8001/api/v1/chat?query=your+question
```

### API Documentation
Open http://localhost:8001/docs for interactive API docs

## ⚡ Performance

### Free Tier Limits
- **Rate Limit**: ~1000 requests/hour
- **Response Time**: 2-5 seconds per query
- **Concurrent Requests**: Limited to avoid rate limits

### Tips for Better Performance
1. **Batch uploads**: Upload multiple documents at once
2. **Cache results**: The system caches embeddings in ChromaDB
3. **Shorter queries**: More concise queries = faster responses
4. **Off-peak hours**: Less traffic = faster responses

## 🐛 Troubleshooting

### "Invalid API key" Error
- Verify your token at https://huggingface.co/settings/tokens
- Make sure you copied the entire token
- Check that HF_API_KEY in .env has no extra spaces

### "Rate limit exceeded" Error
- Wait a few minutes before retrying
- The free tier has hourly limits
- Consider upgrading to Hugging Face Pro ($9/month) for higher limits

### "Model not found" Error
- Some models require acceptance of terms
- Visit the model page on Hugging Face and accept terms
- Example: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

### Slow Responses
- First request to a model is slower (cold start)
- Subsequent requests are faster
- Consider using smaller models for faster responses

## 📈 Upgrading

### To Hugging Face Pro ($9/month)
- Higher rate limits
- Priority access to models
- Faster inference
- Sign up at https://huggingface.co/pricing

### To Self-Hosted (Free but requires GPU)
- Install Ollama: https://ollama.ai
- Run models locally
- No rate limits
- Requires good GPU (8GB+ VRAM recommended)

## 🎓 Learning Resources

- **Hugging Face Docs**: https://huggingface.co/docs
- **Inference API**: https://huggingface.co/docs/api-inference
- **Model Hub**: https://huggingface.co/models
- **Mistral Docs**: https://docs.mistral.ai

## 🎉 You're All Set!

Your RAG chatbot is now running with completely free Hugging Face models!

**Next Steps:**
1. Add your HF API key to `.env`
2. Restart the backend
3. Upload some documents
4. Start chatting!

**Questions?**
- Check the API docs: http://localhost:8001/docs
- Read Hugging Face docs: https://huggingface.co/docs
- Experiment with different models!

Enjoy your free, powerful RAG chatbot! 🚀
