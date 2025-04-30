import base64
import json

from fastapi import HTTPException, Request


def parse_jwt_payload(token: str) -> dict:
    try:
        payload = token.split(".")[1]
        padding = "=" * (-len(payload) % 4)  # Base64URLパディング調整
        decoded = base64.urlsafe_b64decode(payload + padding)
        return json.loads(decoded)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid JWT format")


async def get_current_user(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = auth_header.split(" ")[1]
    claims = parse_jwt_payload(token)
    return claims
