import hashlib
import hmac
from urllib.parse import parse_qs


def verify_telegram_init_data(init_data: str, bot_token: str) -> bool:
    if not init_data:
        return False

    parsed = parse_qs(init_data)
    data_check_str = "\n".join(
        f"{k}={v[0]}" for k, v in sorted(parsed.items()) if k != "hash"
    )
    hash_value = parsed.get("hash", [None])[0]
    if not hash_value:
        return False

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check_str.encode(), hashlib.sha256).hexdigest()

    return computed_hash == hash_value
