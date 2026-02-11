# Example: User Registration API

## Input

Request to design a user registration endpoint with validation, database persistence, and error handling.

## Output

### API Design Spec

**Endpoint**: `POST /api/v1/users/register`

**Request Schema (UserRegisterRequest)**

```python
from pydantic import BaseModel, EmailStr, Field

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=255)
```

**Response Schema (UserResponse)**

```python
from datetime import datetime
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str
    created_at: datetime
```

### Route Implementation

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.database import get_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
) -> UserResponse:
    """Register a new user account."""
    try:
        user = await UserService.register_user(db, request)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

### Service Layer (Business Logic)

```python
from app.repositories.user_repository import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    async def register_user(
        db: Session,
        request: UserRegisterRequest
    ) -> UserResponse:
        """Register a new user with validation."""
        # Check for existing user
        existing_user = await UserRepository.get_by_email(db, request.email)
        if existing_user:
            raise ValueError(f"User with email {request.email} already exists")

        # Hash password
        hashed_password = pwd_context.hash(request.password)

        # Create user
        user = await UserRepository.create(
            db,
            email=request.email,
            password_hash=hashed_password,
            full_name=request.full_name
        )

        return UserResponse.from_orm(user)
```

## Context

This example demonstrates:

- Proper Pydantic schema separation (Request/Response)
- Async/await usage in FastAPI routes
- Dependency injection for database sessions
- Service layer pattern with business logic separation
- Error handling with appropriate HTTP status codes
- Password hashing for security

## Effectiveness

- **Type Safety**: ✓ All functions have type hints
- **Schema-First**: ✓ Schemas defined before logic
- **Dependency Injection**: ✓ Database session injected via `Depends()`
- **Service Layer**: ✓ Business logic separated from route
- **Error Handling**: ✓ Centralized with custom exceptions

**Notes**: This pattern is production-ready and follows FastAPI best practices for scalable applications.
