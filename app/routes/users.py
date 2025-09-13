from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.models import Users
from app.database import get_db
from app.schemas.schemas import UserCreate, UserResponse, PaginationUsersResponse, UserEdit
from app.utils.api_key import get_api_key
from app.utils.password_hashed import hash_password

router = APIRouter(prefix="/users", tags=["users"])

# GET
@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(get_api_key)])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1),
) -> PaginationUsersResponse:
    
    result = await db.execute(select(Users).offset(skip).limit(limit).order_by(Users.id.desc()))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return {"total_users": len(users), "users": users}

# Get user by id
@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(get_api_key)])
async def get_user_id(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User by id {user_id} not found")
    return user

# POST
@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_api_key)])
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    
    existing_user = await db.execute(select(Users).where(Users.email == user.email))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    ## hashing the password
    password_hash = hash_password(user.password)
    user = Users(email=user.email, password_hash=password_hash)
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# PUT
@router.put("/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_api_key)])
async def update_user(
    user_id: int,
    user: UserEdit,
    db: AsyncSession = Depends(get_db)) -> UserResponse:

    db_user = await db.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# DELETE
@router.delete("/{user_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_api_key)])
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)) -> dict:

    db_user = await db.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(db_user)
    await db.commit()
    return {"detail": f"User {user_id} deleted"}