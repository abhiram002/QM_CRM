from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, Optional
from pymongo import MongoClient
from bson import ObjectId
from typing import List
from pymongo import UpdateOne
from typing import Dict

app = FastAPI()

client =  MongoClient("mongodb+srv://harsha:harsha@cluster0.fny6tjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["crm"]
users_collection = db["data"]

class UserCreate(BaseModel):
    email: str
    phone_number: str
    usergroup: str
    prod_type: str
    twitterid: Optional[str] = None
    instagramid:Optional[str] = None
    facebookid:Optional[str] = None
    youtubeid:Optional[str] = None
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
async def get_data():
    datas = users_collection.find()
    result =[]
    for data in datas:
        result.append(data)
    return result

@app.get("/customer/{usergroup}", response_model=List[UserCreate])
async def get_users_by_usergroup(usergroup: str):
    users = users_collection.find({"usergroup": usergroup})
    result = []
    for user in users:
        result.append(user)
    return result

@app.get("/userdata/{data}", response_model=List[UserCreate])
async def get_users_by_email_ph(data: str):
    users = users_collection.find({
        "$or": [
            {"email": data},
            {"phone_number": data}
        ]
    })

    result = [user for user in users]
    return result

from fastapi.responses import JSONResponse

@app.put("/editcrm/{value}", response_model=None)
async def update_user(value: str, data: Dict):
    existing_user = users_collection.find_one({"$or": [
            {"email": value},
            {"phone_number": value}
        ]})
    if not existing_user:
        return JSONResponse(content={"message": "User not found"})
    if existing_user:
        users_collection.update_one({"$or": [
                {"email": value},
                {"phone_number": value}
            ]}, {"$set": data})
        
        return JSONResponse(content={"message": "User updated successfully"})

@app.delete("/delete/")
async def delete_user(email: str, phone_number: str, usergroup: str):
    delete_result = users_collection.delete_one({
        "email": email,
        "phone_number": phone_number,
        "usergroup": usergroup
    })
   
    if delete_result.deleted_count == 0:
        return JSONResponse(content={"message": "User not found"})
 
    return JSONResponse(content={"message": "User deleted successfully"})

@app.post("/")
async def post_data(data: UserCreate):

    is_present = users_collection.find_one({
        "email": data.email,
        "phone_number": data.phone_number,
        "usergroup": data.usergroup
    })
    
    if is_present:
        #if data already exists, then its going to update the new values which are enterd by the user......
        updated_data = {}
        for field, value in data.model_dump().items():
            if field == "prod_type":
                continue
            elif value is not None: 
                updated_data[field] = value
            else:
                updated_data[field] = is_present.get(field) #if new value is none.. thn keep the existing data as it is....
        
        # Update the document in MongoDB
        users_collection.update_one({
            "email": data.email,
            "phone_number": data.phone_number,
            "usergroup": data.usergroup
        }, {"$set": updated_data})
        
        return JSONResponse(content={"message": "User Data Already Present.. Data Updated Successfully.."})
    
    else:
        # Insert the new data
        users_collection.insert_one(data.model_dump())
        return JSONResponse(content={"message": "User data inserted successfully"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
