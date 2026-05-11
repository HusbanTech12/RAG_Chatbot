from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from core.database import Base


class Conversation(Base):
    """SQLAlchemy model for conversations."""

    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """SQLAlchemy model for messages."""

    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to conversation
    conversation = relationship("Conversation", back_populates="messages")


class ConversationMemory:
    """Manages conversation history and memory."""

    def __init__(self):
        """Initialize conversation memory."""
        pass

    async def create_conversation(
        self,
        db,
        title: Optional[str] = None
    ) -> Conversation:
        """
        Create a new conversation.

        Args:
            db: Database session
            title: Optional conversation title

        Returns:
            Created conversation
        """
        conversation = Conversation(title=title or "New Conversation")
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation

    async def add_message(
        self,
        db,
        conversation_id: uuid.UUID,
        role: str,
        content: str
    ) -> Message:
        """
        Add a message to a conversation.

        Args:
            db: Database session
            conversation_id: Conversation ID
            role: Message role ('user' or 'assistant')
            content: Message content

        Returns:
            Created message
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    async def get_conversation(
        self,
        db,
        conversation_id: uuid.UUID
    ) -> Optional[Conversation]:
        """
        Get a conversation by ID.

        Args:
            db: Database session
            conversation_id: Conversation ID

        Returns:
            Conversation or None
        """
        from sqlalchemy import select

        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    async def get_conversation_history(
        self,
        db,
        conversation_id: uuid.UUID,
        limit: int = 50
    ) -> List[Message]:
        """
        Get conversation message history.

        Args:
            db: Database session
            conversation_id: Conversation ID
            limit: Maximum number of messages to return

        Returns:
            List of messages
        """
        from sqlalchemy import select

        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_recent_messages(
        self,
        db,
        conversation_id: uuid.UUID,
        n: int = 10
    ) -> List[Dict]:
        """
        Get recent messages for context.

        Args:
            db: Database session
            conversation_id: Conversation ID
            n: Number of recent messages

        Returns:
            List of message dictionaries
        """
        messages = await self.get_conversation_history(db, conversation_id, limit=n)

        return [
            {
                'role': msg.role,
                'content': msg.content
            }
            for msg in messages[-n:]
        ]

    async def list_conversations(
        self,
        db,
        limit: int = 50,
        offset: int = 0
    ) -> List[Conversation]:
        """
        List all conversations.

        Args:
            db: Database session
            limit: Maximum number of conversations
            offset: Offset for pagination

        Returns:
            List of conversations
        """
        from sqlalchemy import select

        result = await db.execute(
            select(Conversation)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def delete_conversation(
        self,
        db,
        conversation_id: uuid.UUID
    ):
        """
        Delete a conversation and all its messages.

        Args:
            db: Database session
            conversation_id: Conversation ID
        """
        from sqlalchemy import delete

        await db.execute(
            delete(Conversation).where(Conversation.id == conversation_id)
        )
        await db.commit()
