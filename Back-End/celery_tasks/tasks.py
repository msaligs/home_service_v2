from celery import shared_task
from application.model import Category, Professional, Location, User, db
import flask_excel as excel
from datetime import datetime

from application.model import IST



@shared_task(ignore_result=False)
def export_category():
    categories = Category.query.all()
    # column_names1 = Category.__table__.columns.keys()

    column_names = [column.name for column in Category.__table__.columns]
    csv_out = excel.make_response_from_query_sets(categories, column_names=column_names, file_type="csv")

    file_path = "celery_tasks/downloads/cat_file.csv"
    with open(file_path,"wb") as file:
        file.write(csv_out.data)
    return "cat_file.csv"

@shared_task(ignore_result=False)
def export_professional():
    professionals = db.session.query(Professional).all()
    # professionals = Professional.query.all()

    # Extract column names from the Professional table
    column_names = [column.name for column in Professional.__table__.columns]

    selected_columns = {
            "professional": ["rating","experience","available","status","status_updated_at"],  # Example: Fetch all columns from Professional
            "category": ["name"],  # Example: Only fetch category_name from Category
            "location": ["city", "state"],  # Example: Fetch city and state from Location
            "user": ["name", "email","mobile","active","created_at"],  # Example: Fetch name and email from User
        }

    # Flatten all column names into one list
    all_column_names = [f"professional.{col}" for col in selected_columns["professional"]] + \
                        [f"category.{col}" for col in selected_columns["category"]] + \
                        [f"location.{col}" for col in selected_columns["location"]] + \
                        [f"user.{col}" for col in selected_columns["user"]]

    # Convert each row to a dictionary, including related columns
    data = []
    for prof in professionals:
        row = {f"professional.{col}": getattr(prof, col, None) for col in selected_columns["professional"]}  # Professional fields
        row.update({f"category.{col}": getattr(prof.category, col, None) for col in selected_columns["category"]})
        row.update({f"location.{col}": getattr(prof.location, col, None) for col in selected_columns["location"]})
        row.update({f"user.{col}": getattr(prof.user, col, None) for col in selected_columns["user"]})
        data.append(row)

    # Generate CSV file
    csv_out = excel.make_response_from_records(data, column_names=all_column_names, file_type="csv")

    # Save file
    time = datetime.now(IST).strftime("%Y-%m-%d %H:%M")
    file_path = f"celery_tasks/downloads/professional_{time}.csv"
    with open(file_path, "wb") as file:
        file.write(csv_out.data)

    return f"professional_{time}.csv"



# @shared_task(ignore_result=False)
# def export_professional():
#     professional = Professional.query.all()
#     column_names = Professional.__table__.columns.keys()
#     professional_data = excel.make_response_from_query_sets(professional, column_names=column_names, file_type="csv")

#     time = datetime.now(IST).strftime("%Y-%m-%d %H:%M")
#     file_path = f"celery_tasks/downloads/professional_{time}.csv"
#     with open(file_path,"wb") as file:
#         file.write(professional_data.data)
#     return f"professional_{time}.csv"


