import base64
import json
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("access")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")  # JSONで構造化
handler.setFormatter(formatter)
logger.addHandler(handler)


def parse_jwt_username(token: str) -> str:
    try:
        payload = token.split(".")[1]
        padding = "=" * (-len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload + padding)
        claims = json.loads(decoded)
        return claims.get("cognito:username", "unknown")
    except Exception as e:
        logger.warning(f"[JWT Decode Error] {repr(e)}")
        return "unknown"


class AccessLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
        # print("Headers:", dict(request.headers))
        path = request.url.path
        query = dict(request.query_params)
        method = request.method
        client_ip = request.client.host
        headers = dict(request.headers)

        auth_header = headers.get("authorization", "")
        token = auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else ""
        # print("token:", token)
        username = parse_jwt_username(token)

        body = None
        if method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                body = body.decode("utf-8")[:500]  # 長すぎる場合は切る
            except Exception:
                body = "unreadable"

        log_entry = {
            "api": method + " " + path,
            "query": query,
            "user": username,
            "ip": client_ip,
        }

        if body:
            log_entry["body"] = body

        try:
            response = await call_next(request)
            log_entry["status"] = response.status_code
            logger.info(json.dumps(log_entry))
            return response
        except Exception as e:
            log_entry["status"] = 500
            log_entry["error"] = repr(e)
            logger.error(json.dumps(log_entry))
            raise
