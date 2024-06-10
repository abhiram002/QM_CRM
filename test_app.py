from fastapi.testclient import TestClient
<<<<<<< HEAD
from main import app

client = TestClient(app)

=======
from crm import app
 
client = TestClient(app)
 
>>>>>>> 23dfe8b3723967b565f25afa31f7d610f3b224cb
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
<<<<<<< HEAD
=======
 

def test_post_data_with_same_email_ph_diff_usergroup():
    data = {
        "email": "example@example.com",
        "phone_number": "9876543210",
        "usergroup": "diff_customer",
        "prod_type": "product",
        "firstname": "John",
        "lastname": "Doe",
        "gender": "Male",
        "date_of_birth": "1990-01-01"
    }
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User data inserted successfully"} 

def test_post_data_with_same_email_usergroup_diff_phone():
    data = {
        "email": "example@example.com",
        "phone_number": "1234567890",
        "usergroup": "customer",
        "prod_type": "product",
        "firstname": "John",
        "lastname": "Doe",
        "gender": "Male",
        "date_of_birth": "1990-01-01"
    }
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User data inserted successfully"}

def test_post_data_with_same_ph_usergroup_diff_email():
    data = {
        "email": "diff_example@example.com",
        "phone_number": "9876543210",
        "usergroup": "diff_customer",
        "prod_type": "product",
        "firstname": "John",
        "lastname": "Doe",
        "gender": "Male",
        "date_of_birth": "1990-01-01"
    }
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User data inserted successfully"}

>>>>>>> 23dfe8b3723967b565f25afa31f7d610f3b224cb

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
<<<<<<< HEAD
=======
 
def test_post_data_existing_user_with_different_prod_type():
    data = {
        "email": "example@example.com",
        "phone_number": "9876543210",
        "usergroup": "customer",
        "prod_type": "new_product",
        "firstname": "John",
        "lastname": "Doe",
        "gender": "Male",
        "date_of_birth": "1990-01-01"
    }
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User Data Already Present.. Data Updated Successfully.."}




########### GET ALL USER DATA ################
>>>>>>> 23dfe8b3723967b565f25afa31f7d610f3b224cb

def test_get_data():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

<<<<<<< HEAD
=======


############# GET USER DATA BY USERGROUP ############### 
>>>>>>> 23dfe8b3723967b565f25afa31f7d610f3b224cb
def test_get_users_by_usergroup():
    usergroup = "customer"
    response = client.get(f"/customer/{usergroup}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
<<<<<<< HEAD

=======
 
>>>>>>> 23dfe8b3723967b565f25afa31f7d610f3b224cb
def test_get_users_by_usergroup_not_found():
    usergroup = "nonexistent"
    response = client.get(f"/customer/{usergroup}")
    assert response.status_code == 200
    assert response.json() == []

<<<<<<< HEAD
def test_get_users_by_email_ph_email():
    data = "example@example.com"
    response = client.get(f"/userdata/{data}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_users_by_email_ph_phone():
=======


############# GET USER DATA USENG EMAIL OR PHONE NUMBER ###############

def test_get_users_by_email():
    email = "example@example.com"
    response = client.get(f"/userdata/{email}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
 
def test_get_users_by_ph_phone():
>>>>>>> 23dfe8b3723967b565f25afa31f7d610f3b224cb
    phone = "1234567890"
    response = client.get(f"/userdata/{phone}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
<<<<<<< HEAD

=======
 
>>>>>>> 23dfe8b3723967b565f25afa31f7d610f3b224cb
def test_get_users_by_email_ph_not_found():
    data = "nonexistent"
    response = client.get(f"/userdata/{data}")
    assert response.status_code == 200
    assert response.json() == []

<<<<<<< HEAD
def test_update_user():
    value= "example@example.com"
   
    usergroup = "customer"
    data = {"firstname": "John", "lastname": "Doe"}
    response = client.put(f"/editcrm/?value={value}&usergroup={usergroup}", json=data)
   
    
 
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}

# def test_update_user_not_found():
#     value = "exampleeee"
#     data = {"firstname": "John", "lastname": "Doe"}
#     response = client.put(f"/editcrm/{value}", json=data)
#     assert response.status_code == 404
#     assert response.json() == {"message":"User not found"}


def test_update_user_not_found():
    value= "exampleeee@example.com"
    usergroup = "customer"
    data = {"firstname": "John", "lastname": "Doe"}
    response = client.put(f"/editcrm/?value={value}&usergroup={usergroup}", json=data)
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

=======

################# UPDATE #####################

def test_update_userfields_using_email():
    value = "example@example.com"
    data = {"firstname": "John", "lastname": "Doe"}
    response = client.put(f"/editcrm/{value}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}

def test_update_userfields_using_phonenumber():
    value = "9876543210"
    data = {"firstname": "John", "lastname": "Doe"}
    response = client.put(f"/editcrm/{value}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}    

def test_update_user_phonenumber_using_email():
    value = "example@example.com"
    data = {"phone_number": "1234567890"}
    response = client.put(f"/editcrm/{value}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}

def test_update_user_email_using_phonenumber():
    value = "1234567890"
    data = {"email": "updatedexample@exmaple.com"}
    response = client.put(f"/editcrm/{value}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}

def test_update_user_email_using_email():
    value = "updatedexample@exmaple.com"
    data = {"email": "example@exmaple.com"}
    response = client.put(f"/editcrm/{value}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}

def test_update_user_phonenumber_using_phonenumber():
    value = "1234567890"
    data = {"phone_number": "9876543210"}
    response = client.put(f"/editcrm/{value}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}

def test_update_user_not_found():
    value = "nonexistent"
    data = {"firstname": "John", "lastname": "Doe"}
    response = client.put(f"/editcrm/{value}", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "User not found"}


############ DELETE ##################

def test_delete_user():
    email = "example@exmaple.com"
    phone_number = "9876543210"
    usergroup = "customer"
    
    response = client.delete(f"/delete/?email={email}&phone_number={phone_number}&usergroup={usergroup}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
 
def test_delete_user_not_found():
    email = "updatedexample@exmaple.com"
    phone_number = "9876543210"
    usergroup = "customer"
    response = client.delete(f"/delete/?email={email}&phone_number={phone_number}&usergroup={usergroup}")
    assert response.status_code == 200
    assert response.json() == {"message": "User not found"}
>>>>>>> 23dfe8b3723967b565f25afa31f7d610f3b224cb
