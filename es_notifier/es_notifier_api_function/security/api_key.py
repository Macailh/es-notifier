from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    return api_key
