from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from services.models import Users


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create_account(self, data) -> Users:
        """
        Create new user account
        """
        new_user = Users(**data.model_dump())

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user


    async def get_user(self, email) -> Users:
        """
        Create new user account
        """
        result = await self.db.execute(select(Users).where(Users.email == email))
        user = result.scalar_one_or_none()

        return user
    
    
    async def get_users(self) -> Users:
        """
        Create new user account
        """
        result = await self.db.execute(select(Users))
        user = result.scalars().all()

        return user
    

    async def set_user_active(self, email: str, is_active: bool) -> dict:
        """
        Change user active status
        """
        result = await self.db.execute(select(Users).where(Users.email == email))
        user = result.scalar_one_or_none()

        if not user:
            return {"error": "User not found"}

        user.is_active = is_active
        await self.db.commit()

        status = "activated" if is_active else "deactivated"
        return {"message": f"Account {email} {status} successfully"}



    async def delete_account(self, email: str) -> dict:
        """
        Delete user account
        """
        result = await self.db.execute(
            select(Users).where(Users.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            return {"error": "User not found"}

        await self.db.delete(user)
        await self.db.commit()

        return {"message": f"Account {email} deleted successfully"}
