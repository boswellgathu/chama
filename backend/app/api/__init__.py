from fastapi import APIRouter

from app.api.endpoints import users, fines, savings, loans, instalments

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(fines.router, prefix="/fines", tags=["fines"])
api_router.include_router(savings.router, prefix="/savings", tags=["savings"])
api_router.include_router(loans.router, prefix="/loans", tags=["loans"])
api_router.include_router(instalments.router, prefix="/instalments", tags=["instalments"])
