from fastapi import Request, Depends
from sqlalchemy.orm import Session

def get_db(request: Request) -> Session:
    return request.state.db
