from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
# Your RSA public key in PEM format goes here
-----END PUBLIC KEY-----"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
# Your RSA private key in PEM format goes here
-----END RSA PRIVATE KEY-----"""

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
