from db_handler.models import Customer


def get_customer_by_email(email):
    customer = Customer.query.filter_by(email=email).first()
    return customer
