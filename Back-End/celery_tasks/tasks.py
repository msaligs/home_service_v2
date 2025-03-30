from flask import render_template
from celery import shared_task
from application.model import Category, Professional, Location, User, db,ServiceRequest, StatusEnum
import flask_excel as excel
from datetime import datetime, timedelta
from celery_tasks.mail_service import send_email

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


@shared_task(ignore_result=False)
def send_welcome_email(to_email, user_name):
    """Send a welcome email using a Jinja template."""
    subject = "Welcome to Home Service"
    
    # Render the Jinja template
    email_body = render_template("welcome_email.html", user_name=user_name)

    # Send the email
    send_email(subject, email_body, to_email)
    

@shared_task(ignore_result=True)
def send_daily_service_request_emails():
    """Fetch users who booked a service today and send them an email with their service status."""
    today = datetime.now().date()

    users = db.session.query(User).join(ServiceRequest).filter(ServiceRequest.status not in  [StatusEnum.REJECTED,StatusEnum.ACCEPTED]).all()

    for user in users:

        service_requests = db.session.query(ServiceRequest).filter(ServiceRequest.status not in  [StatusEnum.REJECTED,StatusEnum.ACCEPTED]).all()

        if service_requests:
            service_requests_data = [
                {
                    "service_name": req.service.name,
                    "status": req.status.value,  # Convert Enum to string
                    "date": req.request_date.strftime("%Y-%m-%d")
                }
                for req in service_requests
            ]

            email_body = render_template("daily_service_email.html", 
                                         user_name=user.name, 
                                         service_requests=service_requests_data)
            send_email(
                subject="Your Daily Service Request Status",
                body=email_body,
                to_email=user.email
            )



@shared_task(ignore_result=True)
def send_monthly_service_request_emails():
    """Fetch users who booked a service in the last 1 month and send them an email with their service status."""
    today = datetime.now().date()
    one_month_ago = today - timedelta(days=30)

    users = db.session.query(User).join(ServiceRequest).filter(ServiceRequest.request_date >= one_month_ago).all()

    for user in users:
        service_requests = (
            db.session.query(ServiceRequest)
            .filter(ServiceRequest.user_id == user.id, ServiceRequest.request_date >= one_month_ago)
            .all()
        )

        if service_requests:
            service_requests_data = [
                {
                    "service_name": req.service.name,
                    "status": req.status.value,  # Convert Enum to string
                    "request date": req.request_date.strftime("%Y-%m-%d"),
                    "completion date": req.completition_date.strftime("%Y-%m-%d") if req.completition_date else None,
                    "professional_name": req.professional.user.name if req.professional else None,
                    "city": req.locaation.city,
                    "price": f"${req.total_price:.2f}",
                }
                for req in service_requests
            ]

            email_body = render_template(
                "monthly_service_email.html", 
                user_name=user.name, 
                service_requests=service_requests_data
            )

            send_email(
                subject="Your Monthly Service Request Summary",
                body=email_body,
                to_email=user.email
            )
            print(f"Email sent to {user.email} with monthly service request summary.")