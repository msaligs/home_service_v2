from main import db, app
from sqlalchemy import select
from application.sec import datastore
from application.model import *
from faker import Faker
from werkzeug.security import generate_password_hash

fake = Faker('en_IN')
with app.app_context():

    db.drop_all()
    db.create_all()
    print("Database created")

    

# Creating the Roles
    datastore.find_or_create_role(name='admin', description='Administrator to manage the system and onboard users and professionals')
    datastore.find_or_create_role(name='user', description='User to request for services')
    datastore.find_or_create_role(name='professional', description='Professional to provide services')

    datastore.commit()
    print("Roles created")



# Adding the admin data to user table
    print("Adding the admin user to user table")
    user1 = datastore.create_user(name='Admin',email='admin@email.in',password = generate_password_hash('Admin'),mobile='1234567890',active=True,roles=['admin'])
    user3 = datastore.create_user(name='User',email='user@email.in',password = generate_password_hash('User'),mobile='12345690',active=True,roles=['user'])
    user2 = datastore.create_user(name='Msaligs',email='msaligs@email.in',password = generate_password_hash('Msaligs'),mobile='12567890',active=True,roles=['professional'])

    try:
        datastore.commit()
        print("Admin created")
    except Exception as e:
        print(f"An error occurred: {e}")



# Adding the professional data to user table
    print("Adding the professional data to user table")
    for _ in range(20):
        user = datastore.create_user(name=fake.name(), email=fake.email(), password=generate_password_hash('zaqxsw123'), mobile=fake.phone_number(),active=False, roles=['professional'] )
    try:
        datastore.commit()
        print("Professional created")
    except Exception as e:
        print(f"An error occurred: {e}")


# Adding the User data to user table
    print("Adding the user data to user table")
    for _ in range(20):
        user = datastore.create_user(name=fake.name(), email=fake.email(), password=generate_password_hash('zaqxsw123'), mobile=fake.phone_number(),roles=['user'],active=False)
    try:
        datastore.commit()
        print("User created")
    except Exception as e:
        print(f"An error occurred: {e}")



# Adding data to categories table using Faker
    print("Adding data to categories table using Faker")
    # for i in range(10):
    with open('category1.csv') as f:
        for line in f.readlines():
            name = line.strip()
            category = Category(name=name, description=fake.catch_phrase(),image_url=fake.image_url())
            db.session.add(category)
    try:
        db.session.commit()
        print("Categories created")
    except Exception as e:
        print(f"An error occurred: {e}")




# Adding data to services table using Faker
    print("Adding data to services table using Faker")
    for _ in range(500):
        service = Service(name=fake.job(), description=fake.catch_phrase(), image_url=fake.image_url(), category_id=fake.random_int(min=1, max=73), time_required=fake.random_int(min=10, max=200,step=5), base_price=fake.random_int(min=100, max=1000,step=10))
        db.session.add(service)
    try:
        db.session.commit()
        print("Services created")
    except Exception as e:
        print(f"An error occurred: {e}")
    

# Adding data to locations table using Faker
    print("Adding data to locations table using Faker")
    for _ in range(25):
        location = Location(city=fake.city(), state=fake.state(), pincode=fake.postcode())
        db.session.add(location)
    try:
        db.session.commit()
        print("Locations created")
    except Exception as e:
        print(f"An error occurred: {e}")


# Adding data to Professional table using Faker
    print("Adding data to Professional table using Faker")
    for i in range(3,23):
        professional = Professional(user_id=i, category_id=fake.random_int(min=1, max=73), location_id=fake.random_int(min=1, max=50), rating=fake.random_int(min=1, max=5,step=1), experience=fake.random_int(min=1, max=10), available=fake.boolean(chance_of_getting_true=60,), image_url=fake.image_url())
        db.session.add(professional)
    try:
        db.session.commit()
        print("Professional data addedd successfully")
    except Exception as e:
        print(f"Something somewhere goes wrong :{e}")




# Adding data to ServiceLocation table   --> total entries = #categories * #location --> 73 * 50 = 3650
    print("Adding data to ServiceLocation table")
    for i in range(1,74): #categories
        for j in range(1,51):
            servlo =  ServiceLocation(category_id = i, location_id = j, surcharge = fake.random_int(min=10,max=600, step=10),active=fake.boolean(chance_of_getting_true=70))
            db.session.add(servlo)
    try:
        db.session.commit()
        print("Service Location data entered")
    except Exception as e:
        print(f"Somewhere something goes wrong: {e}")
    

# adding USER ADDRESS data
    print("Adding User Address data")
    for i in range(24,45):
        useradd = UserAddress(user_id = i,address = fake.address(), city = fake.city_name(),state = fake.state(),pincode = fake.postcode())
        db.session.add(useradd)
    try:
        db.session.commit()
        print("user address data entered successfully")
    except Exception as e:
        print(f"Somewhere something goes wrong: {e}")

    
