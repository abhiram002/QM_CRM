from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from pymongo import MongoClient
from bson import ObjectId
from typing import List

app = FastAPI()

client = MongoClient("mongodb+srv://harsha:harsha@cluster0.fny6tjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["crm"]
users_collection = db["data"]

class UserCreate(BaseModel):
    email: str
    phone_number: str
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
    crmcreatedtime: datetime = datetime.now()
    payment_information: str = ""
    order_history: str = ""
    preferences: str = ""
    communication_preferences: str = ""
    preferred_language: str = ""
    membership_status: str = ""
    reviews_and_ratings: str = ""
    customer_service_interactions: str = ""
    alternate_phone_number: Optional[int] = None

class UserUpdate(BaseModel):
    additional_fields: Optional[Dict[str, Any]] = None

@app.get("/", response_model=List[UserCreate])
async def get_users():
    todos = users_collection.find()
    return [data for data in todos]

@app.get("/{usergroup}", response_model=List[UserCreate])
async def get_users_by_usergroup(usergroup: str):
    users = users_collection.find({"usergroup": usergroup})
    return [user for user in users]

@app.get("/item/{data}", response_model=List[UserCreate])
async def get_users_by_email_ph(data: str):
    users = users_collection.find({"$or": [{"email": data}, {"phone_number": data}]})
    return [user for user in users]

@app.post("/")
async def create_user(data: UserCreate):
    users_collection.insert_one(data.dict())

@app.put("/{user_id}")
async def update_user(user_id: str, data: UserUpdate):
    # Check if the user exists
    if not users_collection.find_one({"_id": ObjectId(user_id)}):
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user document
    update_data = {}
    if data.additional_fields:
        update_data.update(data.additional_fields)
    
    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return {"message": "User updated successfully"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
