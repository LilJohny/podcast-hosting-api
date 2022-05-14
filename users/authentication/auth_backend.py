from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

PUBLIC_KEY = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDDoh+YiKptTTuhIx6BwRAKOPsytpbq6suvYlcFrSxwjBjJ5rQvOMwliG4wVDOXf17pFG6M0g8qHetL7vy8lHJmrjnj50+X31Y8+nG6uXSxHch3PP+DscCBw7+e7u7fDVaaU6y+ARlsEmjsMnbQYxRwjSbqIIWSpHb5z3jOG9SACzZdOmW0+TOhb3wNVrAHsMffI8fvchLI6mwAVlPMhZ5WGL36rYbyfL8p0QF1kD2Enigj2uLmLX1aOzEa4QFfrFuKi3zQBCATUojN3H7msuRBIAp2Czsqtqcj6RPLwNWzW1cNiCLoTM7zTz3gSEiUeRGh59qqxXSv94QqysI3dJMHAebMz5gpLshnSboJsgauMVZ4qlYNp72cEA1de8wHfQZloKYJngQmyKv++5Jz/mWpaRhUIFIOAnOqg5zSRZsS5cbtNQVcA5+iL3yzlOdjAtBMo7paxp9O2MLyWpCG2Ra8a1ufT9JjkYJvNDtUluKa0p/V6TJxJaohhay7qzjqTBU= denis@Deniss-MacBook-Pro.local"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
"""

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=PRIVATE_KEY,
        lifetime_seconds=3600,
        algorithm="RS256",
        public_key=PUBLIC_KEY,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)