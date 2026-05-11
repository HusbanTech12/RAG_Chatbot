'use client';

export default function TypingIndicator() {
  return (
    <div className="w-full bg-gray-50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-800">
      <div className="max-w-3xl mx-auto px-4 py-6 flex gap-4">
        {/* Avatar */}
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-sm flex items-center justify-center text-white font-semibold bg-green-600">
            AI
          </div>
        </div>

        {/* Typing Animation */}
        <div className="flex-1 flex items-center">
          <div className="flex space-x-2">
            <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
        </div>
      </div>
    </div>
  );
}
