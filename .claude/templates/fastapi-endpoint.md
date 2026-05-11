# FastAPI Endpoint Template

Use this template when creating new API endpoints in the backend.

## Basic Endpoint

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/v1", tags=["resource"])

# Request/Response Models
class ResourceCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ResourceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: str

# Endpoints
@router.post("/resources", response_model=ResourceResponse, status_code=201)
async def create_resource(resource: ResourceCreate):
    """
    Create a new resource.
    
    Args:
        resource: Resource creation data
        
    Returns:
        Created resource with ID and timestamp
        
    Raises:
        HTTPException: 400 if validation fails
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/resources", response_model=List[ResourceResponse])
async def list_resources(
    skip: int = 0,
    limit: int = 10
):
    """
    List all resources with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of resources
    """
    # Implementation here
    pass

@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: str):
    """
    Get a specific resource by ID.
    
    Args:
        resource_id: Resource identifier
        
    Returns:
        Resource details
        
    Raises:
        HTTPException: 404 if resource not found
    """
    # Implementation here
    resource = None  # Fetch from database
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: str, resource: ResourceCreate):
    """
    Update an existing resource.
    
    Args:
        resource_id: Resource identifier
        resource: Updated resource data
        
    Returns:
        Updated resource
        
    Raises:
        HTTPException: 404 if resource not found
    """
    # Implementation here
    pass

@router.delete("/resources/{resource_id}", status_code=204)
async def delete_resource(resource_id: str):
    """
    Delete a resource.
    
    Args:
        resource_id: Resource identifier
        
    Raises:
        HTTPException: 404 if resource not found
    """
    # Implementation here
    pass
```

## With Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Validate JWT token and return current user.
    
    Args:
        credentials: Bearer token from Authorization header
        
    Returns:
        User information
        
    Raises:
        HTTPException: 401 if token is invalid
    """
    token = credentials.credentials
    # Validate token and get user
    user = None  # Decode JWT and fetch user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user

@router.post("/protected", response_model=ResourceResponse)
async def protected_endpoint(
    resource: ResourceCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Protected endpoint requiring authentication.
    """
    # Implementation here
    pass
```

## With Database

```python
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_db() -> AsyncSession:
    """Database session dependency."""
    async with async_session() as session:
        yield session

@router.post("/resources", response_model=ResourceResponse)
async def create_resource(
    resource: ResourceCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create resource with database access."""
    # Use db session
    pass
```

## Register Router

In `main.py`:

```python
from fastapi import FastAPI
from .routers import resource_router

app = FastAPI()

app.include_router(resource_router.router)
```
