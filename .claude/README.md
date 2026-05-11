# Claude Agents and Skills

This directory contains specialized agents and skills for the RAG Chatbot project. These provide focused expertise in different areas of development.

## How to Use

Invoke agents using the Agent tool in Claude Code:

```
Agent({
  subagent_type: "agent-name",
  prompt: "Your task description",
  description: "Brief description"
})
```

## Important Documentation

- **[RAG Architecture Guide](RAG_ARCHITECTURE_GUIDE.md)** - Comprehensive guide to different RAG architectures, comparison, and recommendations for this project
- **[Quick Start](QUICKSTART.md)** - Get the project running quickly
- **[Development Roadmap](ROADMAP.md)** - Phased development plan
- **[Project Summary](SUMMARY.md)** - Complete .claude directory overview

## Available Agents

### 🔧 Development Agents

#### `backend-dev`
**FastAPI backend development specialist**
- FastAPI routing, middleware, dependency injection
- Python 3.12 features and async/await patterns
- API design and Pydantic models
- Database integration with SQLAlchemy
- Testing with pytest

**Use when:** Building or modifying backend API endpoints, adding FastAPI features, working with Python code

#### `frontend-dev`
**Next.js frontend development specialist**
- Next.js 16.2.4 App Router (with breaking changes awareness)
- React 19 components and hooks
- TypeScript and type safety
- Tailwind CSS v4 styling
- Chat UI implementation

**Use when:** Building or modifying frontend components, working with Next.js features, styling with Tailwind

#### `fullstack-integrator`
**Specialist in integrating FastAPI backend with Next.js frontend**
- API client setup and type safety
- CORS configuration
- Real-time communication (WebSockets, SSE)
- Authentication flow
- Error handling across the stack

**Use when:** Connecting frontend to backend, implementing API communication, setting up streaming responses

#### `rag-architect`
**RAG architecture specialist**
- Vector databases (ChromaDB, Pinecone, Qdrant, Weaviate, FAISS)
- Embedding models and strategies
- Retrieval strategies and optimization
- Chunking strategies
- RAG patterns and evaluation

**Use when:** Designing or implementing RAG features, choosing vector databases, optimizing retrieval quality

#### `test-engineer`
**Testing specialist for both frontend and backend**
- pytest for backend (async tests, fixtures, mocking)
- Jest and React Testing Library for frontend
- E2E testing with Playwright/Cypress
- Coverage analysis
- RAG-specific testing strategies

**Use when:** Writing tests, setting up test infrastructure, improving test coverage

#### `devops-engineer`
**DevOps specialist for deployment and CI/CD**
- Docker and docker-compose
- CI/CD pipelines (GitHub Actions)
- Cloud deployment strategies
- Monitoring and logging
- Secrets management

**Use when:** Setting up Docker, creating CI/CD pipelines, deploying to production, configuring monitoring

#### `docs-writer`
**Technical documentation specialist**
- API documentation (OpenAPI/Swagger)
- Code documentation (docstrings, comments)
- User documentation (README, guides)
- Architecture documentation
- Changelog and release notes

**Use when:** Writing or updating documentation, creating guides, documenting APIs

---

## Available Skills

### 🔍 Analysis & Review Skills

#### `code-reviewer`
**Reviews code for quality, security, and best practices**
- Code quality assessment
- Security vulnerability identification
- Performance issue detection
- Testing coverage review
- Documentation completeness

**Use when:** Reviewing pull requests, auditing code quality, getting feedback on implementations

#### `security-auditor`
**Audits code for security vulnerabilities**
- OWASP Top 10 vulnerabilities
- Authentication and authorization issues
- Input validation and injection prevention
- Dependency vulnerability scanning
- RAG-specific security (prompt injection, etc.)

**Use when:** Security review before deployment, auditing authentication, checking for vulnerabilities

#### `performance-optimizer`
**Analyzes and optimizes application performance**
- Backend performance (response time, throughput)
- Frontend performance (Core Web Vitals, bundle size)
- Database query optimization
- RAG-specific optimizations (vector search, LLM calls)
- Performance testing and monitoring

**Use when:** Application is slow, optimizing for production, reducing costs, improving user experience

#### `debug-helper`
**Helps diagnose and fix bugs**
- Systematic debugging process
- Common issue patterns (FastAPI, Next.js, RAG)
- Error message interpretation
- Debugging tools and techniques
- Root cause analysis

**Use when:** Encountering bugs, errors, or unexpected behavior

#### `database-specialist`
**Database design and optimization specialist**
- SQL and NoSQL database design
- Vector database setup and optimization
- Schema design for RAG applications
- Query optimization and indexing
- Migration strategies

**Use when:** Designing database schema, optimizing queries, setting up vector databases, database migrations

#### `ui-ux-designer`
**UI/UX design specialist for chat interfaces**
- Chat interface patterns and best practices
- Responsive design (mobile-first)
- Accessibility (WCAG compliance)
- Loading and error states
- Design tokens and consistency

**Use when:** Designing chat UI, improving user experience, ensuring accessibility, creating responsive layouts

---

## Agent Selection Guide

**Starting a new feature?**
- Backend API → `backend-dev`
- Frontend UI → `frontend-dev`
- RAG functionality → `rag-architect`
- Full-stack feature → `fullstack-integrator`

**Improving existing code?**
- Code quality → `code-reviewer`
- Performance → `performance-optimizer`
- Security → `security-auditor`
- Documentation → `docs-writer`

**Fixing issues?**
- Bugs and errors → `debug-helper`
- Database issues → `database-specialist`
- UI/UX issues → `ui-ux-designer`

**Preparing for production?**
- Testing → `test-engineer`
- Deployment → `devops-engineer`
- Security audit → `security-auditor`
- Documentation → `docs-writer`

---

## Best Practices

1. **Choose the right agent or skill**: Select the one whose expertise matches your task
2. **Provide context**: Give enough information about what you're trying to accomplish
3. **Be specific**: Clear, specific prompts get better results
4. **Combine agents and skills**: Use multiple for complex tasks (e.g., `backend-dev` then `test-engineer`)
5. **Review output**: Always review suggestions before implementing

---

## Contributing

When adding new agents or skills:
1. Create the file in `.claude/agents/` or `.claude/skills/`
2. Use the frontmatter format with name, description, model, and tools
3. Include clear guidelines and examples
4. Update this README with the new agent or skill
5. Test with real tasks
