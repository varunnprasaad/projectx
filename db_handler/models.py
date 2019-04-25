from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Base(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs):
        super(Base, self).__init__(**kwargs)

    def __repr__(self):
        items = ['%s=%r' % (col.name, getattr(self, col.name))
                 for col in self.__table__.columns]
        return "<%s.%s[object at %x] {%s}>" % (self.__class__.__module__,
                                               self.__class__.__name__,
                                               id(self), ','.join(items))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Customer(Base, UserMixin):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(10), default='0000000000')
    password = Column(String(100), nullable=False)

    # Foreign keys
    address_id = Column(Integer, ForeignKey('address.id'), nullable=False)

    # Relationships
    reservations = relationship('Reservation', backref='customer', lazy=True)


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String(100))
    city = Column(String(45))
    state = Column(String(20))
    country = Column(String(100))
    zip = Column(Integer)

    # Relationships
    customers = relationship('Customer', backref='address', lazy=True)
    office = relationship('Office', backref='address', uselist=False)


class Office(Base):
    __tablename__ = "office"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))

    # Foreign keys
    address_id = Column(Integer, ForeignKey('address.id'))

    # Relationships
    vehicles = relationship('Vehicle', backref='office', lazy=True)
    reservations = relationship('Reservation', backref='office', lazy=True)


class Vehicle(Base):
    __tablename__ = "vehicle"

    id = Column(Integer, primary_key=True, autoincrement=True)
    make = Column(String(50))
    model = Column(String(50))
    mileage = Column(Integer)
    availability = Column(Integer, default=1)

    # Foreign keys
    office_id = Column(Integer, ForeignKey('office.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    # Relationships
    reservation = relationship('Reservation', backref='vehicle', uselist=False)


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    features = Column(JSON)
    sample_car = Column(String(50))
    price = Column(Integer)

    # Relationships
    vehicles = relationship('Vehicle', backref='category', lazy=True)


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, autoincrement=True)

    reserved_date = Column(Date, default=datetime.now())
    pickup_date = Column(String(20))
    dropoff_date = Column(String(20))

    # Foreign keys
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    office_id = Column(Integer, ForeignKey('office.id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'), nullable=False)
