from main import db, app
from sqlalchemy import select
from application.model import *
from application.sec import datastore
from faker import Faker
from werkzeug.security import generate_password_hash
import csv


fake = Faker('en_IN')

ax_admin= 1
ax_user = 21
ax_professional = 100
ax_location = 139
ax_category = 21
ax_services = 131



with app.app_context():
    db.drop_all()
    db.create_all()

    print("Database Created Successfully!")

# Creating the Roles
    datastore.find_or_create_role(name='admin', description='Administrator to manage the system and onboard users and professionals')
    datastore.find_or_create_role(name='user', description='User to request for services')
    datastore.find_or_create_role(name='professional', description='Professional to provide services')

    datastore.commit()
    print("Roles created")

# Creating the Admin
    print("Creating the Admin")
    admin = datastore.create_user(name='Admin',email='admin@email.com',password=generate_password_hash('admin123'),mobile='9876543210',active=True,roles=['admin'], profile_img_url = fake.image_url())


# Adding the professional data to user table
    print("Adding the professional data to user table")
    for _ in range(100):
        if _ < 50:
            active = True
        else:
            active = False
        user = datastore.create_user(name=fake.name(), email=fake.email(), password=generate_password_hash('zaqxsw123'), mobile=f"9{fake.random_int(100000000, 999999999)}" ,active=active, roles=['professional'], profile_img_url = fake.image_url() )
    try:
        datastore.commit()
        print("Professional created")
    except Exception as e:
        print(f"An error occurred: {e}")


# Adding the User data to user table
    print("Adding the user data to user table")
    user = datastore.create_user(name=fake.name(), email='msaligs@gmail.com', password=generate_password_hash('asdfasdf'), mobile=f"9{fake.random_int(100000000, 999999999)}" ,roles=['user'],active=True, profile_img_url = fake.image_url())

    for _ in range(20):

        user = datastore.create_user(name=fake.name(), email=fake.email(), password=generate_password_hash('zaqxsw123'), mobile=f"9{fake.random_int(100000000, 999999999)}" ,roles=['user'],active=True, profile_img_url = fake.image_url())
    try:
        datastore.commit()
        print("User created")
    except Exception as e:
        print(f"An error occurred: {e}")


# Adding data to locations table 

    with open('states.csv') as f:
        # to skip the header
        f.readline()

        for line in f.readlines():
            line = line.strip().split(',')
            state = line[0]
            cities = line[1:]
            for city in cities:
                location = Location(city=city, state=state)
                db.session.add(location)
            
    

    try:
        db.session.commit()
        print("Locations created successfully!")
    except Exception as e:
        db.session.rollback()  # Rollback in case of errors
        print(f"An error occurred: {e}")


  
# adding USER ADDRESS data
    print("Adding User Address data")
    for i in range(101,122):
        useradd = UserAddress(user_id = i,address = fake.address(),location_id=fake.random_int(min=1, max=139), pincode = fake.postcode())  #city = fake.city_name(),state = fake.state(),
        db.session.add(useradd)
    try:
        db.session.commit()
        print("user address data entered successfully")
    except Exception as e:
        print(f"Somewhere something goes wrong: {e}")

   
# Adding data to ServiceLocation table   --> total entries = #categories * #location --> 73 * 50 = 3650 ---------> 21 * 139 = 2919
    print("Adding data to ServiceLocation table")
    for i in range(1,22): #categories
        for j in range(139): #locations
            servlo =  ServiceLocation(category_id = i, location_id = j, active=fake.boolean(chance_of_getting_true=70))
            db.session.add(servlo)
    try:
        db.session.commit()
        print("Service Location data entered")
    except Exception as e:
        print(f"Somewhere something goes wrong: {e}")
    

# Adding data to Professional table using Faker
    print("Adding data to Professional table using Faker")
    for i in range(1,100):
        professional = Professional(user_id=i, category_id=fake.random_int(min=1, max=21), location_id=fake.random_int(min=1, max=139), rating=fake.pyfloat(min_value=0, max_value=5, right_digits=2), experience=fake.random_int(min=1, max=10), available=fake.boolean(chance_of_getting_true=60,))
        db.session.add(professional)
    try:
        db.session.commit()
        print("Professional data addedd successfully")
    except Exception as e:
        print(f"Something somewhere goes wrong :{e}")




# ######################################################################################
def insert_categories_and_services():
    with open('cat_serv.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        category_dict = {}  # Store categories with their IDs
        
        print("Adding data to categories table using Faker")
        for row in reader:
            category_name = row[0]
            services = row[1:]

            # Insert category if not exists
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(
                    name=category_name,
                    description=fake.catch_phrase(),
                    image_url=fake.image_url(),
                    created_at=datetime.now()
                )
                db.session.add(category)
                db.session.commit()  # Commit to get the category ID
                print(f"Category created: {category_name}")
            
            category_dict[category_name] = category.id  # Store category ID
        
        print("Adding data to services table using Faker")
        with open('cat_serv.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            
            for row in reader:
                category_name = row[0]
                services = row[1:]
                
                for service_name in services:
                    existing_service = Service.query.filter_by(name=service_name, category_id=category_dict[category_name]).first()
                    if not existing_service:
                        service = Service(
                            name=service_name,
                            description=fake.catch_phrase(),
                            image_url=fake.image_url(),
                            category_id=category_dict[category_name],
                            base_price=fake.random_int(min=100, max=1000, step=10),
                            created_at=datetime.now()
                        )
                        db.session.add(service)
            
            db.session.commit()
            print("Services created")

# Run the function within Flask app context
with app.app_context():
    insert_categories_and_services()

print("Data inserted successfully!")
