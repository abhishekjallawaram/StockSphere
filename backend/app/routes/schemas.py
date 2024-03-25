from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, Field

# Base user schema for common attributes
class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr  # Use EmailStr for automatic email validation
    password: constr(min_length=8)  # Enforce minimum length for security

    # OTP related fields with default values
    otp_enabled: bool = False
    otp_verified: bool = False
    otp_base32: str | None = None
    otp_auth_url: str | None = None

    # Automatically set creation and update times
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True

# Schema for user login, utilizing Pydantic's EmailStr for validation
class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)  # Ensure password has a minimum length of 8 for security

# Schema for operations requiring a user's ID and an optional token
class UserRequestSchema(BaseModel):
    user_id: str
    token: str | None = None
