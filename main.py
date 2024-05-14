from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List

app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb+srv://harsha:harsha@cluster0.fny6tjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["crm"]
users_collection = db["data"]

# Pydantic models
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

class UserCreate(BaseModel):
    email: str
    phone_number: int
    usergroup: str
    prod_type: str
    twitterid: str
    category: str = ""
    subcategory: str = ""
    firstname: str
    lastname: str
    gender: str
    date_of_birth: str
    address: str = ""
    crmroles: str = ""
    crmcreatedtime: str
    payment_information: str = ""
    order_history: str = ""
    preferences: str = ""
    communication_preferences: str = ""
    preferred_language: str = ""
    membership_status: str = ""
    reviews_and_ratings: str = ""
    customer_service_interactions: str = ""
    alternate_phone_number: int = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Route to create user
@app.post("/create_user", response_model=UserCreate)
async def create_user(user: UserCreate):
    new_user = dict(user)
    result = await users_collection.insert_one(new_user)
    new_user["_id"] = result.inserted_id
    return new_user

# Route to get users by usergroup
@app.get("/get_users_by_usergroup/{usergroup}", response_model=List[UserCreate])
async def get_users_by_usergroup(usergroup: str):
    users = []
    async for user in users_collection.find({"usergroup": usergroup}):
        # user["_id"] = str(user["_id"])  # Convert ObjectId to string
        users.append(user)
    return users


# Run the application on port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True,reload=True)
