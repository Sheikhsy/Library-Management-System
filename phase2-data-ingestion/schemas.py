from pydantic import BaseModel, field_validator, model_validator
import re
from typing import Optional, Literal
from datetime import datetime, date

import logging

logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


#Library Model
class Library1(BaseModel):
    library_id:int
    name:str
    campus_location:str
    contact_email:str
    phone_number:str

    @field_validator("library_id", mode="before")
    def validate_id(cls, v):
        if  v <= 0:
            raise ValueError("ID must be a positive integer")
        return v

    @field_validator("name",mode="before")
    def clean_name(cls,v):
        char_only = re.sub(r"\d", "", v)
        return ' '.join(char_only.strip().split()).title()

    @field_validator("contact_email")
    def email_pattern(cls, v:str)->str:
        pattern=r"^[\w\.-]+@[\w\.]+.\w{2,}$"
        if not re.match(pattern,v):
            raise ValueError("Invalid Email!")
        return v

    @field_validator("phone_number",mode="before")
    def phone_number_validation(cls,v:str)->str:
        if not v.isdigit():
            raise ValueError("Phone number must contain digits only.")
        if len(v.strip())<10:
            raise ValueError("Phone Numbers can't be less than 10 digits")

        digits_only = re.sub(r"\D", "", v)
        core_number = digits_only[-10:]

        if len(core_number) != 10:
            raise ValueError("Phone number must have 10 digits after removing country code.")

        return f"+91-{core_number[0:3]}-{core_number[3:6]}-{core_number[6:]}"

#Book Model
class Book(BaseModel):
    Book_id:int
    Libray_id:int
    title: str
    isbn: str
    publication_date: date
    total_copies: int
    available_copies: int

    @field_validator("title")
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("isbn")
    def validate_isbn(cls, v: str) -> str:
        pattern = r"^(97(8|9))?\d{9}(\d|X)$"
        if not re.match(pattern, v.replace("-", "")):
            raise ValueError("Invalid ISBN format")
        return v

    @field_validator("available_copies")
    def cant_be_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Available copies cannot be negative")
        return v

    @field_validator("publication_date", mode="before")
    def parse_and_validate_date(cls, v: str) -> date:
        try:
            return datetime.strptime(v, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Date must be in format DD-MM-YYYY (e.g., 29-07-2025)")

    @model_validator(mode="after")
    def check_copies_consistency(self) -> "Book":
        if self.available_copies > self.total_copies:
            raise ValueError("Available copies cannot exceed total copies")
        return self

#Borrowing Model
class Borrowing(BaseModel):
    borrowing_id:int
    borrow_date: date
    due_date: date
    return_date: date
    late_fee: float
    book_id:int
    member_id:int


    @field_validator("borrowing_id", mode="before")
    def validate_borrow_id(cls, v:int)->int:
        if not isinstance(v, int) or v <= 0:
            raise ValueError("ID must be a positive integer")
        return v

    @field_validator("borrow_date", mode="before")
    def parse_and_validate_borrow_date(cls, v: str) -> date:
        try:
                return datetime.strptime(v, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Date must be in format DD-MM-YYYY (e.g., 29-07-2025)")

    @field_validator("due_date", mode="before")
    def parse_and_validate_due_date(cls, v: str) -> date:
        try:
                return datetime.strptime(v, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Date must be in format DD-MM-YYYY (e.g., 29-07-2025)")

    @field_validator("return_date", mode="before")
    def parse_and_validate_return_date(cls, v: str) -> date:
        try:
                return datetime.strptime(v, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Date must be in format DD-MM-YYYY (e.g., 29-07-2025)")


    @field_validator("book_id", mode="before")
    def validate_book_id(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError("ID must be a positive integer")
        return v

    @field_validator("member_id", mode="before")
    def validate_mem_id(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError("ID must be a positive integer")
        return v

    @model_validator(mode="after")
    def validate_dates(self) -> "Borrowing":
        if self.due_date < self.borrow_date:
            raise ValueError("Due date cannot be before borrow date.")

        if self.return_date:
            if self.return_date < self.borrow_date:
                raise ValueError("Return date cannot be before borrow date.")
        return self

#Member Model
class Member(BaseModel):
    member_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    member_type: Literal["Student", "Faculty"]
    registration_date: date


    @field_validator("first_name", mode="before")
    def normalize_first_name(cls, v: str) -> str:
        return ' '.join(v.strip().split()).title()
    @field_validator("last_name", mode="before")
    def normalize_last_name(cls, v: str) -> str:
        return ' '.join(v.strip().split()).title()

    @field_validator("phone", mode="before")
    def validate_phone_number(cls, v: str) -> str:
        digits = re.sub(r"\D", "", v)  # Remove non-digit characters
        if len(digits) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        return f"+91-{digits[0:3]}-{digits[3:6]}-{digits[6:]}"  # Format it

    # Join date should not be in the future
    @field_validator("registration_date")
    def validate_join_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Join date cannot be in the future.")
        return v
    @field_validator("email")
    def email_pattern(cls, v:str)->str:
        pattern=r"^[\w\.-]+@[\w\.]+\.\w{2,}$"
        if not re.match(pattern,v):
            raise ValueError("Invalid Email!")
        return v
    # Ensure ID is a positive integer
    @field_validator("member_id")
    def validate_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Member ID must be a positive integer.")
        return v

#Author Model
class Author(BaseModel):
    author_id: int
    first_name: str
    last_name: str
    email: str| None
    phone_number: Optional[str] = None
    nationality: Optional[str] = None
    biography: Optional[str] = None

    # Validate ID
    @field_validator("author_id")
    def validate_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Author ID must be a positive integer.")
        return v

    # Normalize first name
    @field_validator("first_name", mode="before")
    def normalize_first_name(cls, v: str) -> str:
        return ' '.join(v.strip().split()).title()

    @field_validator("last_name", mode="before")
    def normalize_last_name(cls, v: str) -> str:
        return ' '.join(v.strip().split()).title()

    @field_validator("nationality", mode="before")
    def normalize_nationality(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return ' '.join(v.strip().split()).title()
        return v

    @field_validator("biography", mode="before")
    def normalize_bio(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return ' '.join(v.strip().split())
        return v

    @field_validator("phone_number", mode="before")
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v:
            digits = re.sub(r"\D", "", v)
            if len(digits) != 10:
                raise ValueError("Phone number must be 10 digits if provided.")
            return f"+91-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        return v

class Review(BaseModel):
    review_id: int
    member_id: int
    book_id: int
    rating:int
    comment:str
    review_date: date

    @field_validator("review_id")
    def validate_review_id(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Review ID must be a positive integer.")
        return v

    # Validate rating range (0 to 5)
    @field_validator("rating")
    def validate_rating(cls, v: int) -> int:
        if not (1 <= v <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return v

    # Normalize and clean comment
    @field_validator("comment", mode="before")
    def normalize_comment(cls, v: str) -> str:
        return ' '.join(v.strip().split())

    # Optionally validate review_date not in the future
    @field_validator("review_date")
    def validate_review_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Review date cannot be in the future.")
        return v

class Category(BaseModel):
    category_id:int
    name: str
    description: Optional[str] = None

    @field_validator("name")
    def name_must_not_be_blank(cls, v:str)->str:
        if not v.strip():
            raise ValueError("Category name must not be blank")
        return v
