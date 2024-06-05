from fastapi.testclient import TestClient
from crm import app
 
client = TestClient(app)
 
def test_post_data_new_user():
    data = {
        "email": "example@example.com",
        "phone_number": "9876543210",
        "usergroup": "customer",
        "prod_type": "product",
        "firstname": "Jane",
        "lastname": "Doe",
        "gender": "Female",
        "date_of_birth": "1995-01-01"
    }
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User data inserted successfully"}
 
def test_post_data_existing_user():
    data = {
        "email": "example@example.com",
        "phone_number": "9876543210",
        "usergroup": "customer",
        "prod_type": "product",
        "firstname": "John",
        "lastname": "Doe",
        "gender": "Male",
        "date_of_birth": "1990-01-01"
    }
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User Data Already Present.. Data Updated Successfully.."}
 
def test_get_data():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
 
def test_get_users_by_usergroup():
    usergroup = "customer"
    response = client.get(f"/customer/{usergroup}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
 
def test_get_users_by_usergroup_not_found():
    usergroup = "nonexistent"
    response = client.get(f"/customer/{usergroup}")
    assert response.status_code == 200
    assert response.json() == []
 
def test_get_users_by_email_ph_email():
    email = "example@example.com"
    response = client.get(f"/userdata/{email}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
 
def test_get_users_by_email_ph_phone():
    phone = "1234567890"
    response = client.get(f"/userdata/{phone}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
 
def test_get_users_by_email_ph_not_found():
    data = "nonexistent"
    response = client.get(f"/userdata/{data}")
    assert response.status_code == 200
    assert response.json() == []
 
def test_update_user():
    value = "example@example.com"
    data = {"firstname": "John", "lastname": "Doe"}
    response = client.put(f"/editcrm/{value}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}
 
# def test_update_user_not_found():
#     value = "exampleeee"
#     data = {"firstname": "John", "lastname": "Doe"}
#     response = client.put(f"/editcrm/{value}", json=data)
#     assert response.status_code == 404
#     assert response.json() == {"message":"User not found"}
 
 
def test_update_user_not_found():
    value = "nonexistent"
    data = {"firstname": "John", "lastname": "Doe"}
    response = client.put(f"/editcrm/{value}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User not found"}
 
def test_delete_user():
    email = "example@example.com"
    phone_number = "9876543210"
    usergroup = "customer"
    prod_type = "product"
    response = client.delete(f"/delete/?email={email}&phone_number={phone_number}&usergroup={usergroup}&prod_type={prod_type}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
 
def test_delete_user_not_found():
    email = "example@example.com"
    phone_number = "9876543210"
    usergroup = "customer"
    prod_type = "product"
    response = client.delete(f"/delete/?email={email}&phone_number={phone_number}&usergroup={usergroup}&prod_type={prod_type}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}