# Next.js Component Template

Use this template when creating new React components in the frontend.

## Server Component (Default)

```typescript
// app/components/ServerComponent.tsx
import { ReactNode } from 'react';

interface ServerComponentProps {
  title: string;
  children?: ReactNode;
}

export default function ServerComponent({ title, children }: ServerComponentProps) {
  // Server Components can:
  // - Fetch data directly
  // - Access backend resources
  // - Use async/await
  
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">{title}</h1>
      {children}
    </div>
  );
}
```

## Client Component

```typescript
// app/components/ClientComponent.tsx
'use client';

import { useState, useEffect } from 'react';

interface ClientComponentProps {
  initialValue?: string;
}

export default function ClientComponent({ initialValue = '' }: ClientComponentProps) {
  const [value, setValue] = useState(initialValue);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Side effects here
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/endpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value }),
      });

      if (!response.ok) {
        throw new Error('Request failed');
      }

      const data = await response.json();
      // Handle success
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter value"
        />
        
        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Loading...' : 'Submit'}
        </button>

        {error && (
          <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        )}
      </form>
    </div>
  );
}
```

## Chat Message Component

```typescript
// app/components/ChatMessage.tsx
'use client';

import { memo } from 'react';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

function ChatMessage({ role, content, timestamp }: ChatMessageProps) {
  const isUser = role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[70%] rounded-lg px-4 py-2 ${
          isUser
            ? 'bg-blue-500 text-white'
            : 'bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100'
        }`}
      >
        <div className="prose prose-sm max-w-none">
          {content}
        </div>
        {timestamp && (
          <div className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
            {timestamp.toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
}

export default memo(ChatMessage);
```

## Page Component

```typescript
// app/page-name/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
};

export default function PageName() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-6">Page Title</h1>
      {/* Page content */}
    </main>
  );
}
```

## Layout Component

```typescript
// app/section/layout.tsx
import { ReactNode } from 'react';

export default function SectionLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <aside className="w-64 bg-gray-100 dark:bg-gray-900 p-4">
        {/* Sidebar content */}
      </aside>
      <main className="flex-1 p-8">
        {children}
      </main>
    </div>
  );
}
```

## API Route Handler

```typescript
// app/api/endpoint/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get('query');

    // Process request
    const data = { message: 'Success', query };

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate body
    if (!body.field) {
      return NextResponse.json(
        { error: 'Missing required field' },
        { status: 400 }
      );
    }

    // Process request
    const result = { success: true };

    return NextResponse.json(result, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```
