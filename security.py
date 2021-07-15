from fastapi import HTTPException
from fastapi.param_functions import Header
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_header(secret_key: str = Header(...)):
    _check = os.getenv('secret_key_hash')
    if not pwd_context.verify(secret_key, _check):
        raise HTTPException(status_code=400, detail="Wrong secret!")
