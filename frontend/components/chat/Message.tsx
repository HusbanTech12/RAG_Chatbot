'use client';

import { Message as MessageType } from '@/lib/types';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MessageProps {
  message: MessageType;
}

export default function Message({ message }: MessageProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`w-full border-b border-gray-100 dark:border-gray-800 ${
        isUser
          ? 'bg-white dark:bg-gray-900'
          : 'bg-gray-50 dark:bg-gray-800/50'
      }`}
    >
      <div className="max-w-3xl mx-auto px-4 py-6 flex gap-4">
        {/* Avatar */}
        <div className="flex-shrink-0">
          <div
            className={`w-8 h-8 rounded-sm flex items-center justify-center text-white font-semibold ${
              isUser
                ? 'bg-blue-600'
                : 'bg-green-600'
            }`}
          >
            {isUser ? 'U' : 'AI'}
          </div>
        </div>

        {/* Message Content */}
        <div className="flex-1 min-w-0">
          {isUser ? (
            <p className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap">
              {message.content}
            </p>
          ) : (
            <div className="prose prose-sm max-w-none dark:prose-invert prose-pre:bg-gray-900 prose-pre:text-gray-100">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
