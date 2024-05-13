from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# MongoDB connection
async def connect_to_mongodb():
    client = AsyncIOMotorClient("mongodb://localhost:27017/")
    db = client["schema"]
    return db["CRUD"]

# Dependency to get the MongoDB collection
async def get_collection():
    return await connect_to_mongodb()

# Pydantic model
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
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class CRMUserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    phone_number: int
    usergroup: str
    prod_type: str
    twitterid: str
    category: str
    subcategory: str
    firstname: str
    lastname: str
    gender: str
    date_of_birth: str
    address: str
    crmroles: str
    crmcreatedtime: str
    payment_information: str
    order_history: str
    preferences: str
    communication_preferences: str
    preferred_language: str
    membership_status: str
    reviews_and_ratings: str
    customer_service_interactions: str
    alternate_phone_number: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# GET all CRM based on usergroup
@app.get("/crm", response_model=List[CRMUserModel])
async def get_crm_by_usergroup(usergroup: str, collection = Depends(get_collection)):
    users = await collection.find({"usergroup": usergroup}).to_list(length=None)
    return users

# GET CRM based on usergroup, phone_number, or email
@app.get("/crm/{field}", response_model=List[CRMUserModel])
async def get_customer(field: str, value: str, collection = Depends(get_collection)):
    query = {field: value}
    users = await collection.find(query).to_list(length=None)
    return users

# POST a new CRM
@app.post("/crm", response_model=CRMUserModel)
async def create_crm(user: CRMUserModel, collection = Depends(get_collection)):
    new_user = dict(user)
    result = await collection.insert_one(new_user)
    new_user["_id"] = result.inserted_id
    return new_user

# UPDATE an existing CRM
@app.put("/crm/{user_id}", response_model=CRMUserModel)
async def edit_crm(user_id: str, user: CRMUserModel, collection = Depends(get_collection)):
    update_data = dict(user)
    result = await collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.modified_count == 1:
        updated_user = await collection.find_one({"_id": ObjectId(user_id)})
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")
