import hashlib
import hmac
import secrets

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 260_000
SESSION_MAX_AGE_SECONDS = 7 * 24 * 60 * 60
SESSION_COOKIE_NAME = "agriflow_session"


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM, password.encode("utf-8"), bytes.fromhex(salt), PBKDF2_ITERATIONS
    ).hex()
    return f"pbkdf2_{PBKDF2_ALGORITHM}${PBKDF2_ITERATIONS}${salt}${digest}"


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        algorithm_label, iterations, salt, digest = encoded_hash.split("$")
        algorithm = algorithm_label.removeprefix("pbkdf2_")
        iterations = int(iterations)
    except (ValueError, AttributeError):
        return False

    candidate = hashlib.pbkdf2_hmac(
        algorithm, password.encode("utf-8"), bytes.fromhex(salt), iterations
    ).hex()
    return hmac.compare_digest(candidate, digest)


def _serializer(secret_key: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key, salt="agriflow-session")


def create_session_token(secret_key: str, user_id: int, username: str, role: str) -> str:
    return _serializer(secret_key).dumps({"uid": user_id, "username": username, "role": role})


def read_session_token(secret_key: str, token: str) -> dict | None:
    try:
        return _serializer(secret_key).loads(token, max_age=SESSION_MAX_AGE_SECONDS)
    except (BadSignature, SignatureExpired):
        return None
