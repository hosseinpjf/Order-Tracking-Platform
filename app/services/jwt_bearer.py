from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from app.services.tokens import verify_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        token = auth.credentials

        payload = verify_token(token)
        if payload is None:
            raise HTTPException(status_code=403, detail="Invalid or expired token")
        
        return payload