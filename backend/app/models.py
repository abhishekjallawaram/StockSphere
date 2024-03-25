from pydantic import BaseModel, Field , conint
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return str(ObjectId(v))
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class Agent(BaseModel):
    agent_id: conint(ge=0, le=999999)
    # name: _get_object_size
    name : str  
    contact: str
    level: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda o: str(o)}

    # class Config:
    #     allow_population_by_field_name = True
    #     arbitrary_types_allowed = True
        
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

class Stock(BaseModel):
    stock_id: conint(ge=0, le=999999)
    Company_name: str
    Company_ticker: str
    Closed_price: float
    Company_info: str
    Company_PE: Optional[float] = Field(None, description="Price to Earnings Ratio")
    Company_cash_flow: Optional[float] = Field(None, description="Operating Cash Flow")
    Company_dividend: Optional[float] = Field(None, description="Dividend Rate")


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda o: str(o)}
        populate_by_name  = True
        # orm_mode = True
        
        
        
        
class CreateStockRequest(BaseModel):
    Company_name: str
    Company_ticker: str
    Closed_price: float
    Company_info: str
    Company_PE: Optional[float] = Field(None, description="Price to Earnings Ratio")
    Company_cash_flow: Optional[float] = Field(None, description="Operating Cash Flow")
    Company_dividend: Optional[float] = Field(None, description="Dividend Rate")
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda o: str(o)}
        populate_by_name  = True

        
        



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