# Backend Running on Port 8001 - Next Steps

## ✅ What's Done
- Backend is running on port 8001
- Frontend .env.local updated to point to http://localhost:8001

## 🔄 Restart Frontend

The frontend needs to be restarted to pick up the new environment variable:

```bash
# Stop the frontend (Ctrl+C in the terminal where it's running)
# Then restart it:
cd /mnt/d/Projects/RAG_Chatbot/frontend
npm run dev
```

## 🧪 Test the Connection

Once the frontend restarts, try these tests:

### 1. Check Backend Health
Open in browser: http://localhost:8001/health

Should return:
```json
{
  "status": "healthy",
  "services": {
    "database": "healthy",
    "vector_store": "healthy",
    "embedding_service": "healthy"
  }
}
```

### 2. Check API Docs
Open: http://localhost:8001/docs

You should see the interactive API documentation.

### 3. Test Chat
1. Open http://localhost:3000
2. Click "Start Chatting"
3. Type a message
4. You should see the response streaming in

## ⚠️ Important Notes

### OpenAI API Key Required
The system needs an OpenAI API key to work. If you see errors about missing API key:

1. Get a key from: https://platform.openai.com/api-keys
2. Add to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
3. Restart backend

### Alternative: Use Gemini
Since you have a Gemini API key, I can modify the code to use Google's Gemini instead. Let me know if you'd prefer that!

## 🐛 If You Still Get 404 Errors

1. **Verify backend is running:**
   ```bash
   # Should show the fastapi process
   ps aux | grep fastapi
   ```

2. **Check the logs:**
   Look at the terminal where backend is running for any errors

3. **Verify frontend env:**
   ```bash
   cat /mnt/d/Projects/RAG_Chatbot/frontend/.env.local
   # Should show: NEXT_PUBLIC_API_URL=http://localhost:8001
   ```

4. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
   - Or open in incognito/private window

## 📝 Upload a Test Document

Once everything is working, upload a test document:

```bash
# Create test.txt
echo "RAG (Retrieval-Augmented Generation) combines information retrieval with text generation." > test.txt

# Upload it
curl -X POST -F "file=@test.txt" http://localhost:8001/api/v1/documents/upload
```

Then ask in the chat: "What is RAG?"

## ✨ You're Almost There!

Just restart the frontend and you should be good to go! 🚀
