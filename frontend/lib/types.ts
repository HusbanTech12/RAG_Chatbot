export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Conversation {
  id: string;
  title: string | null;
  created_at: Date;
  updated_at: Date;
  messages: Message[];
}

export interface ChatRequest {
  query: string;
  conversation_id?: string;
  n_results?: number;
}

export interface Source {
  text: string;
  metadata: Record<string, any>;
  score: number;
}

export interface StreamChunk {
  token?: string;
  done: boolean;
  conversation_id?: string;
  sources?: Source[];
  error?: string;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  sources: Source[];
}

export interface Document {
  id: string;
  filename: string;
  uploaded_at: Date;
  chunk_count: number;
  metadata: Record<string, any>;
}

export interface DocumentUploadResponse {
  document_id: string;
  filename: string;
  chunks_created: number;
  message: string;
}
