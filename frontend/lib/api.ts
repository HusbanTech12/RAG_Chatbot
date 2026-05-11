import { ChatRequest, Conversation, StreamChunk } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function* streamChatResponse(
  request: ChatRequest
): AsyncGenerator<StreamChunk, void, unknown> {
  const response = await fetch(`${API_URL}/api/v1/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error('No response body');
  }

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          try {
            const parsed: StreamChunk = JSON.parse(data);
            yield parsed;
          } catch (e) {
            console.error('Error parsing chunk:', e);
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

export async function getConversations(): Promise<Conversation[]> {
  const response = await fetch(`${API_URL}/api/v1/conversations`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.conversations.map((conv: any) => ({
    ...conv,
    created_at: new Date(conv.created_at),
    updated_at: new Date(conv.updated_at),
    messages: conv.messages.map((msg: any) => ({
      ...msg,
      timestamp: new Date(msg.created_at),
    })),
  }));
}

export async function getConversation(id: string): Promise<Conversation> {
  const response = await fetch(`${API_URL}/api/v1/conversations/${id}`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return {
    ...data,
    created_at: new Date(data.created_at),
    updated_at: new Date(data.updated_at),
    messages: data.messages.map((msg: any) => ({
      ...msg,
      timestamp: new Date(msg.created_at),
    })),
  };
}

export async function createConversation(title?: string): Promise<Conversation> {
  const response = await fetch(`${API_URL}/api/v1/conversations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return {
    ...data,
    created_at: new Date(data.created_at),
    updated_at: new Date(data.updated_at),
    messages: [],
  };
}

export async function deleteConversation(id: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/v1/conversations/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
}

export async function uploadDocument(file: File): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_URL}/api/v1/documents/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export async function getDocuments(): Promise<any[]> {
  const response = await fetch(`${API_URL}/api/v1/documents`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data.documents.map((doc: any) => ({
    ...doc,
    uploaded_at: new Date(doc.uploaded_at),
  }));
}

export async function deleteDocument(id: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/v1/documents/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
}
