#DELETE THIS FILE AS IT GENERATE FALSE POSITIVE USE: generate_keywords.py INSTEAD
import re

def generate_keywords(domains):
    keywords = set()
    for domain in domains:
        name = domain.split('.')[0]

        # Add domain and company name-based variations
        keywords.update({
            name,
            domain,
            f"{name}@",
            f"{name}123",
            f"{name}admin",
            f"{name}.com",
            domain.replace('.', ''),
        })
        
        # Add email-related keywords (e.g., company email patterns)
        keywords.update({
            f"{name}@{domain}",
            f"contact@{domain}",
            f"support@{domain}",
            f"info@{domain}",
        })
        
        # Add API key patterns
        keywords.update([
            "sk_", "api_", "token_", "secret_", "auth_", "key_",
            "client_id", "client_secret", "private_key", "access_token"
        ])
        
        # Regex patterns for phone numbers, credit cards, etc.
        keywords.update([
            r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b",  # Phone numbers
            r"\b\d{4}[-.\s]??\d{4}[-.\s]??\d{4}[-.\s]??\d{4}\b"  # Credit card number
        ])
        
        # Add internal project names, if you know them (examples)
        internal_keywords = ["internal", "dev", "api", "secret", "backend", "database", "admin", "login"]
        keywords.update(internal_keywords)
    
    return list(keywords)
