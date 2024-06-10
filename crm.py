from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pymongo import MongoClient
from bson import ObjectId
from typing import List
 
app = FastAPI()
 
client =  MongoClient("mongodb+srv://harsha:harsha@cluster0.fny6tjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
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
 
 
@app.get("/", response_model=List[UserCreate])
async def get_todos():
    todos = users_collection.find()
    result =[]
    for data in todos:
        result.append(data)
    return result
 
@app.get("/{usergroup}", response_model=List[UserCreate])
async def get_users_by_usergroup(usergroup: str):
    users = users_collection.find({"usergroup": usergroup})
    result = []
    for user in users:
        result.append(user)
    return result
 
@app.get("/item/{data}", response_model=List[UserCreate])
async def get_users_by_email_ph(data: str):
    users = users_collection.find({
        "$or": [
            {"email": data},
            {"phone_number": data}
        ]
    })
 
    result = [user for user in users]
    return result
 
@app.post("/")
async def post_data(data: UserCreate):
    users_collection.insert_one(dict(data))
 
@app.put("/items/{item_id}", response_model=UserCreate)
async def update_item(item_id: str, item: UserCreate):
    update_item_encoded = jsonable_encoder(item)
    UserCreate[item_id] = update_item_encoded
    return update_item_encoded
   
   
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)