from sqlalchemy import create_engine,Integer,String,Date,ForeignKey,Column,Enum,TEXT
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base,relationship

try:
    engine = create_engine("mysql+pymysql://root:root@localhost/lb_system", echo=True)
    with engine.connect() as connection:
        print("Connection established successfully.")
except SQLAlchemyError as e:
    print("Connection failed:", e)

Base=declarative_base()
class Library(Base):
    __tablename__ = "libraries"
    library_id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100),nullable=False)
    campus_location=Column(String(100),nullable=False)
    contact_email=Column(String(100),nullable=False)
    phone_number=Column(String(15),nullable=False)
    books=relationship("Book",back_populates="library")

class Book(Base):
    __tablename__="books"
    book_id=Column(Integer,primary_key=True,autoincrement=True)
    library_id=Column(Integer,ForeignKey('libraries.library_id'))
    title=Column(String(200),nullable=False)
    isbn=Column(String(20),unique=True)
    publication_date=Column(Date,nullable=False)
    total_copies=Column(Integer,nullable=False)
    available_copies=Column(Integer,nullable=False)
    library = relationship("Library", back_populates="books")

class Member(Base):
    __tablename__="members"
    member_id=Column(Integer,primary_key=True,autoincreament=True)
    first_name=Column(String(200),nullable=False)
    last_name=Column(String(200),nullable=False)
    email=Column(String(200),nullable=False)
    phone=Column(String(200),nullable=False)
    member_type=Column(Enum("Student", "Faculty", name="member_type_enum"), nullable=False)
    registration_date=Column(Date,nullable=False)

class Author(Base):
    __tablename__ = "members"
    first_name=Column(String(200),nullable=False)
    last_name=Column(String(200),nullable=False)
    birth_date=Column(Date,nullable=False)
    nationality=Column(String(200),nullable=False)
    biography=Column(TEXT,nullable=True)

