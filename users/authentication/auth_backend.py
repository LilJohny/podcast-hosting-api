from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend

from settings import SSH_PUBLIC_KEY, SSH_PRIVATE_KEY

PUBLIC_KEY = SSH_PUBLIC_KEY

PRIVATE_KEY = SSH_PRIVATE_KEY

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
