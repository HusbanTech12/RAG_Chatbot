import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen items-center justify-center bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-black">
      <main className="flex flex-col items-center gap-8 px-8 py-16 text-center max-w-2xl">
        <h1 className="text-5xl font-bold text-gray-900 dark:text-white">
          RAG Chatbot
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300">
          Advanced Conversational AI with Retrieval-Augmented Generation
        </p>
        <p className="text-gray-500 dark:text-gray-400">
          Upload your documents and chat with an AI assistant that understands your content.
          Powered by hybrid search, conversation memory, and intelligent query rewriting.
        </p>

        <div className="flex gap-4 mt-8">
          <Link
            href="/chat"
            className="px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold text-lg"
          >
            Start Chatting
          </Link>
          <Link
            href="/documents"
            className="px-8 py-4 bg-gray-200 dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors font-semibold text-lg"
          >
            Manage Documents
          </Link>
        </div>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
          <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              Hybrid Search
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Combines semantic and keyword search for better accuracy
            </p>
          </div>
          <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              Conversation Memory
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Maintains context across multiple messages
            </p>
          </div>
          <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              Streaming Responses
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Real-time responses as they're generated
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
