from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ExampleEnum(str, Enum):
    OPTION_A = "option_a"
    OPTION_B = "option_b"
    OPTION_C = "option_c"

class AdvancedValidationExample(BaseModel):
    """Example showing advanced Pydantic validation patterns"""
    
    # Field with multiple validators
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    
    # Conditional validation
    age: Optional[int] = Field(None, ge=0, le=150)
    is_adult: Optional[bool] = None
    
    # Custom validation with dependencies
    password: str = Field(..., min_length=8)
    confirm_password: str
    
    # Enum validation
    category: ExampleEnum
    
    # List validation
    tags: List[str] = Field(default_factory=list, max_items=10)
    
    # Dict validation
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('email')
    def validate_email_domain(cls, v):
        """Custom email domain validation"""
        if not v.endswith(('.com', '.org', '.net')):
            raise ValueError('Email must end with .com, .org, or .net')
        return v.lower()
    
    @validator('is_adult', always=True)
    def validate_adult_status(cls, v, values):
        """Conditional validation based on age"""
        age = values.get('age')
        if age is not None:
            return age >= 18
        return v
    
    @validator('tags')
    def validate_tags(cls, v):
        """Validate list items"""
        if v:
            # Remove duplicates and empty strings
            v = list(set(tag.strip() for tag in v if tag.strip()))
            # Validate each tag
            for tag in v:
                if len(tag) < 2:
                    raise ValueError('Each tag must be at least 2 characters long')
        return v
    
    @root_validator
    def validate_passwords_match(cls, values):
        """Root validator for cross-field validation"""
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValueError('Passwords do not match')
        
        return values
    
    class Config:
        # Enable validation on assignment
        validate_assignment = True
        # Use enum values instead of names
        use_enum_values = True
        # Custom JSON encoders
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        # Schema example for documentation
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "age": 25,
                "password": "securepassword123",
                "confirm_password": "securepassword123",
                "category": "option_a",
                "tags": ["python", "fastapi", "pydantic"],
                "metadata": {"source": "api", "version": "1.0"}
            }
        }

class PaginationSchema(BaseModel):
    """Reusable pagination schema"""
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries"""
        return (self.page - 1) * self.size

class PaginatedResponse(BaseModel):
    """Generic paginated response schema"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
    
    @validator('pages', always=True)
    def calculate_pages(cls, v, values):
        """Calculate total pages"""
        total = values.get('total', 0)
        size = values.get('size', 20)
        return (total + size - 1) // size if total > 0 else 0

class FilterSchema(BaseModel):
    """Base filter schema for search endpoints"""
    search: Optional[str] = Field(None, min_length=1, max_length=100)
    sort_by: Optional[str] = Field(None, regex=r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    sort_order: Optional[str] = Field(default="asc", regex=r'^(asc|desc)$')
    
    @validator('search')
    def validate_search(cls, v):
        """Clean search query"""
        if v:
            return v.strip()
        return v
