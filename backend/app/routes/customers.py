from fastapi import APIRouter, HTTPException, Request,Depends
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from typing import List,Optional,Any
import yfinance as yf
from app.models import Customer
from app.routes.schemas import CustomerRequenst,CustomerResponse,UserAuth,TokenSchema
from fastapi import APIRouter, HTTPException
from ..database.mongo import get_collections
from bson import ObjectId
from pymongo.collection import ReturnDocument
from fastapi import APIRouter, HTTPException, status
from app.utils import authutils
from fastapi import APIRouter, HTTPException, Request,Depends


router = APIRouter()
    
    
    
@router.get("/", response_model=list[CustomerResponse])
async def get_customers(user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    customers = await collections["customers"].find(
        {}, 
        {"hashed_password": 0}  
    ).to_list(length=100)
    return [CustomerResponse(**customer) for customer in customers]


# @router.post("/register", response_model=CustomerResponse)
# async def create_customer(customer_request: CustomerRequenst):
#     collections = await get_collections()

#     # Check if the user already exists
#     existing_user = await collections["customers"].find_one({"email": customer_request.email})
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email is already registered"
#         )

#     max_id_doc = await collections["customers"].find_one(sort=[("customer_id", -1)])
#     maxid = max_id_doc['customer_id'] + 1 if max_id_doc and 'customer_id' in max_id_doc else 1

#     hashed_password = securityutils.get_hashed_password(customer_request.hashed_password)
#     customer_data = customer_request.dict(by_alias=True)
#     customer_data["customer_id"] = maxid
#     customer_data["hashed_password"] = hashed_password 
#     res = await collections["customers"].insert_one(customer_data)
#     created_customer = await collections["customers"].find_one({"_id": res.inserted_id})
#     return CustomerResponse(**{k: v for k, v in created_customer.items() if k != 'hashed_password'})



# async def authenticate(username: str, password: str) -> Optional[CustomerResponse]:
#     user = await read_customer_byusername(username=username)
#     if not user:
#         return None
#     if not securityutils.verify_password(password=password, hashed_pass=user.hashed_password):
#         return None
#     return user


# @router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
# async def login(form_data: OAuth2PasswordRequestForm  = Depends()) -> Any:
#     user = await authenticate(username=form_data.username, password=form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password"
#         )
    
#     return {
#         "access_token": securityutils.create_access_token(user.customer_id),
#         "refresh_token": securityutils.create_refresh_token(user.customer_id),
#     }
    
# @router.post('/test-token', summary="Test if the access token is valid", response_model=CustomerResponse)
# async def test_token(user: Customer = Depends(get_current_user)):
#     return user


@router.get("/{customerid}", response_model=Customer)
async def read_customer_byid(customerid: int, user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    item = await collections["customers"].find_one({"customer_id": customerid})
    if item:
        return Customer(**item)
    raise HTTPException(status_code=404, detail="Item not found")





@router.get("/{username}", response_model=Customer)
async def read_customer_byusername(username: str,user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    item = await collections["customers"].find_one({"username": username})
    if item:
        return Customer(**item)
    raise HTTPException(status_code=404, detail="Item not found")






@router.put("/{customerid}", response_model=Customer)
async def update_customer(customerid: int, update_data: CustomerRequenst,user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    updated_stock = await collections["customers"].find_one_and_update(
        {"customer_id": customerid},
        {"$set": update_data.dict(by_alias=True)},
        return_document=ReturnDocument.AFTER
    )

    if updated_stock:
        return Customer(**updated_stock)
    else:
        raise HTTPException(status_code=404, detail="Stock not found")
    




@router.delete("/{customerid}", response_model=dict)
async def delete_customer(customerid: int ,user: Customer = Depends(authutils.get_current_admin)):
    collections = await get_collections()
    delete_result = await collections["customers"].delete_one({"customer_id": customerid})

    if delete_result.deleted_count == 1:
        return {"message": "Stock deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Stock not found")



    
    