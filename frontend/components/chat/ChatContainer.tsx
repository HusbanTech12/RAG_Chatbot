'use client';

import { useState } from 'react';
import { Message as MessageType } from '@/lib/types';
import { streamChatResponse } from '@/lib/api';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import Link from 'next/link';

export default function ChatContainer() {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: MessageType = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Stream response
      let assistantContent = '';
      const assistantMessageId = (Date.now() + 1).toString();

      for await (const chunk of streamChatResponse({
        query: content,
        conversation_id: conversationId,
        n_results: 5,
      })) {
        if (chunk.error) {
          setError(chunk.error);
          break;
        }

        if (chunk.done) {
          // Update conversation ID
          if (chunk.conversation_id) {
            setConversationId(chunk.conversation_id);
          }

          // Final message is already added, just mark as done
          setIsLoading(false);
        } else if (chunk.token) {
          // Append token to assistant message
          assistantContent += chunk.token;

          // Update or add assistant message
          setMessages((prev) => {
            const existing = prev.find((m) => m.id === assistantMessageId);
            if (existing) {
              return prev.map((m) =>
                m.id === assistantMessageId
                  ? { ...m, content: assistantContent }
                  : m
              );
            } else {
              return [
                ...prev,
                {
                  id: assistantMessageId,
                  role: 'assistant' as const,
                  content: assistantContent,
                  timestamp: new Date(),
                },
              ];
            }
          });
        }
      }
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setConversationId(undefined);
    setError(null);
  };

  return (
    <div className="flex flex-col h-screen bg-white dark:bg-gray-900">
      {/* Header */}
      <div className="flex-shrink-0 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h1 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              RAG Chatbot
            </h1>
            {messages.length > 0 && (
              <button
                onClick={handleNewChat}
                className="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              >
                + New Chat
              </button>
            )}
          </div>
          <div className="flex gap-2">
            <Link
              href="/documents"
              className="px-3 py-1.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              📄 Documents
            </Link>
            <Link
              href="/"
              className="px-3 py-1.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              🏠 Home
            </Link>
          </div>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="flex-shrink-0 bg-red-50 dark:bg-red-900/20 border-b border-red-200 dark:border-red-800">
          <div className="max-w-3xl mx-auto px-4 py-3">
            <p className="text-sm text-red-700 dark:text-red-400">{error}</p>
          </div>
        </div>
      )}

      {/* Messages */}
      <MessageList messages={messages} isLoading={isLoading} />

      {/* Input */}
      <div className="flex-shrink-0">
        <MessageInput onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
