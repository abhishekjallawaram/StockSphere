from pydantic import BaseModel, EmailStr, Field, ConfigDict, BaseConfig
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class Agent(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    contact: str
    level: str

    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

# class Customer(BaseModel):
#     id: Optional[PyObjectId] = None
#     name: str
#     email: EmailStr
#     balance: float

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}

# class Stock(BaseModel):
#     id: Optional[PyObjectId] = None
#     name: str
#     ticker: str
#     price_currency: str
#     cash_flow: float

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}

# class StockHistory(BaseModel):
#     id: Optional[PyObjectId] = None
#     name: str
#     ticker: str
#     date: str
#     open: float
#     close: float
#     low: float
#     high: float

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}

# class Transaction(BaseModel):
#     id: Optional[PyObjectId] = None
#     customer_id: PyObjectId
#     stock_id: PyObjectId
#     ticker: str
#     volume: int
#     action: str
#     date: str
#     agent_id: PyObjectId

#     class Config:
#         orm_mode = True
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}