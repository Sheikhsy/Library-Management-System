from sqlalchemy import (Integer,Numeric,String,Date,ForeignKey,Column,Enum,TEXT,
                        CheckConstraint)

from sqlalchemy.orm import declarative_base,relationship

Base=declarative_base()

class Library1(Base):
    __tablename__ = "Library1"
    library_id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100),nullable=False)
    campus_location=Column(String(100),nullable=False)
    contact_email=Column(String(100),nullable=False)
    phone_number=Column(String(100),nullable=False)
    books = relationship("Book", back_populates="library")

class Book(Base):
    __tablename__="Book"
    book_id=Column(Integer,primary_key=True,autoincrement=True)
    library_id=Column(Integer,ForeignKey('Library1.library_id',onupdate="CASCADE"))
    title=Column(String(200),nullable=False)
    isbn=Column(String(20),unique=True)
    publication_date=Column(Date,nullable=False)
    total_copies=Column(Integer,nullable=False)
    available_copies=Column(Integer,nullable=False)
    library = relationship("Library1", back_populates="books")
    borrowings = relationship("Borrowing", back_populates="book")
    book_categories = relationship("BookCategory", back_populates="book")
    book_authors = relationship("BookAuthor", back_populates="book")
    reviews = relationship("Review", back_populates="book")

class Member(Base):
    __tablename__="Member"
    member_id=Column(Integer,primary_key=True,autoincrement=True)
    first_name=Column(String(200),nullable=False)
    last_name=Column(String(200),nullable=False)
    email=Column(String(200),nullable=False)
    phone=Column(String(200),nullable=False)
    member_type=Column(Enum("Student", "Faculty", name="member_type_enum"), nullable=False)
    registration_date=Column(Date,nullable=False)
    borrowings=relationship("Borrowing",back_populates="member")
    reviews = relationship("Review", back_populates="member")

class Author(Base):
    __tablename__ = "Author"
    author_id=Column(Integer,primary_key=True,autoincrement=True)
    first_name=Column(String(200),nullable=False)
    last_name=Column(String(200),nullable=False)
    email=Column(String(200),nullable=False)
    phone_number=Column(String(20),nullable=True)
    nationality=Column(String(200),nullable=False)
    biography=Column(TEXT,nullable=True)
    book_authors = relationship("BookAuthor", back_populates="author")

class Borrowing(Base):
    __tablename__ = "Borrowing"

    borrowing_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("Member.member_id", onupdate="CASCADE"))
    book_id = Column(Integer, ForeignKey("Book.book_id", onupdate="CASCADE"))
    borrow_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date,nullable=True)
    late_fee = Column(Numeric(10, 2))

    member = relationship("Member", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")

class Review(Base):
    __tablename__ = "Review"
    review_id=Column(Integer,primary_key=True,autoincrement=True)
    member_id=Column(Integer,ForeignKey('Member.member_id',onupdate="CASCADE"))
    book_id=Column(Integer,ForeignKey('Book.book_id',onupdate="CASCADE"))
    rating=Column(Integer, nullable=False)
    comment=Column(TEXT,nullable=True)
    review_date=Column(Date,nullable=False)
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )
    member = relationship("Member", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")

class Category(Base):
    __tablename__ = "Category"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(TEXT,nullable=True)

    book_categories = relationship("BookCategory", back_populates="category")

class BookAuthor(Base):
    __tablename__ = "BookAuthor"

    book_id = Column(Integer, ForeignKey("Book.book_id", onupdate="CASCADE"), primary_key=True)
    author_id = Column(Integer, ForeignKey("Author.author_id", onupdate="CASCADE"), primary_key=True)

    book = relationship("Book", back_populates="book_authors")
    author = relationship("Author", back_populates="book_authors")

class BookCategory(Base):
    __tablename__ = "BookCategory"

    book_id = Column(Integer, ForeignKey("Book.book_id", onupdate="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("Category.category_id", onupdate="CASCADE"), primary_key=True)

    book = relationship("Book", back_populates="book_categories")
    category = relationship("Category", back_populates="book_categories")



