from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from asgiref.sync import sync_to_async

_password_hasher = PasswordHasher()


async def get_password_hash(password: str) -> str:
    return await _get_password_hash_async(password)


async def verify_password(hashed_password: str, password: str) -> bool:
    return await _verify_password_async(hashed_password, password)


# Here are the "real" implementations, with the "sync_to_async" dance:


def _get_password_hash(password: str) -> str:
    return _password_hasher.hash(password)


_get_password_hash_async = sync_to_async(_get_password_hash, thread_sensitive=False)


def _verify_password(hashed_password: str, password: str) -> bool:
    try:
        _password_hasher.verify(hashed_password, password)
    except VerifyMismatchError:
        return False
    return True


_verify_password_async = sync_to_async(_verify_password, thread_sensitive=False)
