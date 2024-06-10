from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from jose import JWTError, jwt
from fastapi.responses import JSONResponse
from passlib.context import CryptContext # type: ignore
 
# JWT settings
SECRET_KEY = "crm"  # Change this to a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
 
app = FastAPI()
 
client = MongoClient("mongodb+srv://harsha:harsha@cluster0.fny6tjl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["crm"]
users_collection = db["users"]
data_collection = db["data"]
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
 
class UserCreate(BaseModel):
    email: str
    phone_number: str
    usergroup: str
    prod_type: str
    twitterid: Optional[str] = None
    instagramid: Optional[str] = None
    facebookid: Optional[str] = None
    youtubeid: Optional[str] = None
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
 
class UserRegister(BaseModel):
    username: str
    password: str
    usergroup: str
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
 
async def get_current_usergroup(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usergroup: str = payload.get("usergroup")
       
        if usergroup is None:
            raise credentials_exception
       
        # Check if token has expired
        exp = payload.get("exp")
        if exp is None or datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise credentials_exception
 
        return usergroup
    except JWTError:
        raise credentials_exception
 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
 
def get_password_hash(password):
    return pwd_context.hash(password)
 
@app.post("/register", response_model=dict)
async def register_user(username: str, password:str,usergroup:str):
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already registered")
   
    user_data = {
        "username": username,
        "hashed_password": get_password_hash(password),
        "usergroup": usergroup
    }
    users_collection.insert_one(user_data)
    return {"message": "User registered successfully"}
 
@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
 
    usergroup = user["usergroup"]
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "usergroup": usergroup}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
 
@app.get("/customer", response_model=List[UserCreate])
async def get_users_by_usergroup(usergroup: str = Depends(get_current_usergroup)):
    users = data_collection.find({"usergroup": usergroup})
    result = []
    for user in users:
        result.append(user)
    return result
 
@app.get("/userdata/{data}", response_model=List[UserCreate])
async def get_users_by_email_ph(data: str, usergroup: str = Depends(get_current_usergroup)):
    users = data_collection.find({
        "$and": [
            {"$or": [
                {"email": data},
                {"phone_number": data}
            ]},
            {"usergroup": usergroup}
        ]
    })
    result = [user for user in users]
    return result
 
@app.put("/editcrm/{value}", response_model=None)
async def update_user(value: str, data: Dict, usergroup: str = Depends(get_current_usergroup)):
    existing_user = data_collection.find_one({
        "$and": [
            {"$or": [
                {"email": value},
                {"phone_number": value}
            ]},
            {"usergroup": usergroup}
        ]
    })
    if not existing_user:
        return JSONResponse(content={"message": "User not found"})
    if existing_user:
        data_collection.update_one({
            "$and": [
                {"$or": [
                    {"email": value},
                    {"phone_number": value}
                ]},
                {"usergroup": usergroup}
            ]}, {"$set": data})
        return JSONResponse(content={"message": "User updated successfully"})
 
@app.delete("/delete/")
async def delete_user(email: str, phone_number: str, usergroup: str = Depends(get_current_usergroup)):
    delete_result = data_collection.delete_one({
        "email": email,
        "phone_number": phone_number,
        "usergroup": usergroup
    })
    if delete_result.deleted_count == 0:
        return JSONResponse(content={"message": "User not found"})
    return JSONResponse(content={"message": "User deleted successfully"})
 
@app.post("/")
async def post_data(data: UserCreate, usergroup: str = Depends(get_current_usergroup)):
    if data.usergroup != usergroup:
        raise HTTPException(status_code=400, detail="Invalid usergroup")
 
    is_present = data_collection.find_one({
        "email": data.email,
        "phone_number": data.phone_number,
        "usergroup": data.usergroup
    })
   
    if is_present:
        updated_data = {}
        for field, value in data.model_dump().items():
            if field == "prod_type":
                continue
            elif value is not None:
                updated_data[field] = value
            else:
                updated_data[field] = is_present.get(field)
       
        data_collection.update_one({
            "email": data.email,
            "phone_number": data.phone_number,
            "usergroup": data.usergroup
        }, {"$set": updated_data})
       
        return JSONResponse(content={"message": "User Data Already Present.. Data Updated Successfully.."})
   
    else:
        data_collection.insert_one(data.model_dump())
        return JSONResponse(content={"message": "User data inserted successfully"})
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
 