from datetime import datetime
import pyotp
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument
from fastapi import APIRouter, status, HTTPException, Depends

from ..database.mongo import get_user as async_get_user
from ..routes import schemas

router = APIRouter()

# Dependency to normalize email and check for existing user
async def get_user_by_email(email: str, check_existence: bool = False):
    User = await async_get_user()
    normalized_email = email.lower()
    user = await User.find_one({'email': normalized_email})
    if check_existence and user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exists')
    return normalized_email, user

# Dependency to validate ObjectId and fetch user
async def get_user_by_id(user_id: str):
    User = await async_get_user()
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {user_id}")
    
    user = await User.find_one({'_id': ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')
    return userEntity(user)

def userEntity(user) -> dict:
    return {key: str(value) if key == "_id" else value for key, value in user.items()}

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.UserBaseSchema):
    User = await async_get_user()
    email, existing_user = await get_user_by_email(payload.email, check_existence=False)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exists')
    # Proceed with your logic since no user was found with this email
    payload.email = email
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at
    await User.insert_one(payload.dict())
    return {'status': 'success', 'message': "Registered successfully, please login"}

@router.post('/login')
async def login(payload: schemas.LoginUserSchema):
    User = await async_get_user()
    email, user = await get_user_by_email(payload.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect Email or Password')
    return {'status': 'success', 'user': userEntity(user)}

@router.post('/otp/generate')
async def generate_otp(payload: schemas.UserRequestSchema, user: dict = Depends(get_user_by_id)):
    User = await async_get_user()
    otp_base32 = pyotp.random_base32()
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(name="admin@admin.com", issuer_name="YourAppName")
    await User.find_one_and_update({'_id': ObjectId(payload.user_id)}, {'$set': {"otp_auth_url": otp_auth_url, "otp_base32": otp_base32}}, return_document=ReturnDocument.AFTER)
    return {'base32': otp_base32, "otpauth_url": otp_auth_url}

@router.post('/otp/verify')
async def verify_otp(payload: schemas.UserRequestSchema, user: dict = Depends(get_user_by_id)):
    User = await async_get_user()
    if not pyotp.TOTP(user.get("otp_base32")).verify(payload.token):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid or user doesn't exist")
    await User.find_one_and_update({'_id': ObjectId(payload.user_id)}, {'$set': {"otp_enabled": True, "otp_verified": True}}, return_document=ReturnDocument.AFTER)
    return {'otp_verified': True, "user": user}

@router.post('/otp/validate')
async def validate_otp(payload: schemas.UserRequestSchema, user: dict = Depends(get_user_by_id)):
    User = await async_get_user()
    if not user.get("otp_verified"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP must be verified first")
    if not pyotp.TOTP(user.get("otp_base32")).verify(otp=payload.token, valid_window=1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid or user doesn't exist")
    return {'otp_valid': True}

@router.post('/otp/disable')
async def disable_otp(payload: schemas.UserRequestSchema, user: dict = Depends(get_user_by_id)):
    User = await async_get_user()
    await User.find_one_and_update({'_id': ObjectId(payload.user_id)}, {'$set': {"otp_enabled": False}}, return_document=ReturnDocument.AFTER)
    return {'otp_disabled': True, 'user': user}
