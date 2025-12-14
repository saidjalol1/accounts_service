from typing import List

from fastapi import Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession

from services.db_conf import get_session
from services.service import UserService
from services.schemas import (
    UserResponse,
    UserUpdate,
    AccountCreateSchema
)

router = InferringRouter()


@cbv(router)
class AccountRoutes:
    db: AsyncSession = Depends(get_session)

    @router.post("/users",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
    async def create_user(self, data: AccountCreateSchema):
        service = UserService(self.db)
        return await service.create_account(data)


    @router.get("/users/{email}",response_model=UserResponse)
    async def get_user(self, email: str):
        service = UserService(self.db)
        user = await service.get_user(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    @router.get("/users",response_model=List[UserResponse])
    async def get_all_users(self):
        service = UserService(self.db)
        return await service.get_users()

    
    @router.patch("/users/{email}/active",status_code=status.HTTP_200_OK)
    async def update_user_active(
        self,
        email: str,
        data: UserUpdate,
    ):
        service = UserService(self.db)
        result = await service.set_user_active(
            email=email,
            is_active=data.is_active,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"],
            )

        return result


    @router.delete("/users/{email}",status_code=status.HTTP_200_OK)
    async def delete_user(self, email: str):
        service = UserService(self.db)
        result = await service.delete_account(email)

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"],
            )

        return result
