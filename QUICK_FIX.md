# Quick Start Guide - Fixing the 404 Error

## Problem
The backend server isn't running, causing 404 errors when the frontend tries to connect.

## Solution

### Option 1: Use OpenAI (Current Implementation)

The system is currently configured for OpenAI. You need an OpenAI API key.

**Get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add it to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

**Start Backend:**
```bash
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
fastapi dev main.py
```

### Option 2: Use Gemini (Requires Code Changes)

Since you have a Gemini API key, I can modify the code to use Google's Gemini instead of OpenAI.

**Would you like me to:**
1. Modify the code to use Gemini for embeddings and LLM?
2. Or get an OpenAI API key and use the current implementation?

## Quick Test (After Starting Backend)

**Terminal 1 - Backend:**
```bash
cd /mnt/d/Projects/RAG_Chatbot/backend
fastapi dev main.py
```

**Terminal 2 - Frontend:**
```bash
cd /mnt/d/Projects/RAG_Chatbot/frontend
npm run dev
```

**Terminal 3 - Test:**
```bash
# Check health
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","services":{...}}
```

## Common Issues

### "Module not found" errors
```bash
cd backend
uv sync
```

### "Port already in use"
```bash
# Kill existing process
pkill -f fastapi
# Or use different port
fastapi dev main.py --port 8001
```

### Frontend still gets 404
- Verify backend is running: http://localhost:8000/docs
- Check frontend .env.local has correct API URL
- Clear browser cache and reload

## Current Status

✅ Backend code implemented
✅ Frontend code implemented
✅ Dependencies installed
❌ Backend not running (need to start it)
⚠️  Need OpenAI API key OR switch to Gemini

Let me know which option you prefer!
