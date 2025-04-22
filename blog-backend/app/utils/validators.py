import re
from typing import Optional

def is_valid_username(username: str) -> bool:
    """
    Validate username format.
    
    Rules:
    - 3-20 characters
    - Alphanumeric characters, underscores, and hyphens only
    - Must start with a letter
    """
    if not username or len(username) < 3 or len(username) > 20:
        return False
        
    pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*$'
    return bool(re.match(pattern, username))

def is_valid_password(password: str) -> bool:
    """
    Validate password strength.
    
    Rules:
    - At least 6 characters
    - Contains at least one digit
    - Contains at least one letter
    """
    if not password or len(password) < 6:
        return False
        
    has_digit = any(char.isdigit() for char in password)
    has_letter = any(char.isalpha() for char in password)
    
    return has_digit and has_letter

def is_valid_slug(slug: str) -> bool:
    """
    Validate slug format.
    
    Rules:
    - Lowercase letters, numbers, and hyphens only
    - Must start and end with a letter or number
    - No consecutive hyphens
    """
    if not slug:
        return False
        
    pattern = r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$'
    return bool(re.match(pattern, slug)) and '--' not in slug

def generate_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from a title.
    
    Args:
        title: The title to convert to a slug
        
    Returns:
        A URL-friendly slug
    """
    # Convert to lowercase
    slug = title.lower()
    
    # Replace non-alphanumeric characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # Replace multiple consecutive hyphens with a single one
    slug = re.sub(r'-+', '-', slug)
    
    return slug
