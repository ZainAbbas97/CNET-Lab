"""
Security utilities: JWT tokens, password hashing, input validation.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Command whitelist (Phase 1.1)
ALLOWED_COMMANDS = {
    "upload_dataset": ["filename"],
    "plot": ["type", "x", "y", "title", "xlabel", "ylabel"],
    "describe": [],
    "corr": [],
    "head": ["n"],
    "tail": ["n"],
    "info": [],
    "statistical_summary": [],
}

# Allowed file extensions
ALLOWED_EXTENSIONS = {".csv"}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> dict:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def validate_command(command: str, params: dict) -> tuple[bool, Optional[str]]:
    """
    Validate command against whitelist (Phase 1.1).
    Returns (is_valid, error_message)
    """
    if command not in ALLOWED_COMMANDS:
        return False, f"Command '{command}' is not allowed. Allowed commands: {', '.join(ALLOWED_COMMANDS.keys())}"
    
    # Validate parameters
    allowed_params = ALLOWED_COMMANDS[command]
    for param in params.keys():
        if param not in allowed_params:
            return False, f"Parameter '{param}' is not allowed for command '{command}'"
    
    return True, None


def sanitize_filename(filename: str) -> tuple[bool, Optional[str]]:
    """
    Sanitize and validate filename (Phase 1.2).
    Returns (is_valid, sanitized_filename or error_message)
    """
    if not filename:
        return False, "Filename cannot be empty"
    
    # Check for path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return False, "Path traversal not allowed"
    
    # Check for absolute paths
    if filename.startswith("/") or (len(filename) > 1 and filename[1] == ":"):
        return False, "Absolute paths not allowed"
    
    # Check extension
    if not any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        return False, f"File type not allowed. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Sanitize: only alphanumeric, dots, underscores, hyphens, spaces
    # Allow spaces in filenames (common in user uploads)
    sanitized = "".join(c for c in filename if c.isalnum() or c in "._- ")
    # Remove leading/trailing spaces but allow spaces in middle
    sanitized = sanitized.strip()
    
    # Check for dangerous characters (but allow spaces)
    dangerous_chars = ['<', '>', '|', '&', ';', '`', '$', '(', ')', '{', '}', '[', ']']
    if any(char in filename for char in dangerous_chars):
        return False, "Filename contains invalid characters"
    
    return True, filename


def validate_file_size(size_bytes: int) -> tuple[bool, Optional[str]]:
    """Validate file size (Phase 1.2)."""
    max_size = settings.max_file_size_mb * 1024 * 1024
    if size_bytes > max_size:
        return False, f"File size exceeds maximum of {settings.max_file_size_mb}MB"
    return True, None


def validate_command_length(command: str) -> tuple[bool, Optional[str]]:
    """Validate command length (Phase 1.2)."""
    max_length = 10 * 1024  # 10KB
    if len(command) > max_length:
        return False, f"Command length exceeds maximum of {max_length} bytes"
    return True, None



