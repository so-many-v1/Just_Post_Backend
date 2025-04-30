import secrets

def generate_verification_email_link():
    return secrets.token_urlsafe(32)
