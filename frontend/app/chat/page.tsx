import ChatContainer from '@/components/chat/ChatContainer';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Chat - RAG Chatbot',
  description: 'Chat with your documents using AI',
};

export default function ChatPage() {
  return <ChatContainer />;
}
