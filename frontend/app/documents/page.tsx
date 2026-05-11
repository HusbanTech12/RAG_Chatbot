import DocumentManager from '@/components/documents/DocumentManager';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Documents - RAG Chatbot',
  description: 'Manage your knowledge base documents',
};

export default function DocumentsPage() {
  return <DocumentManager />;
}
