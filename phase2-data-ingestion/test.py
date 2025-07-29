from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
import re
from datetime import datetime, date

import logging

logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Book(BaseModel):
    title: str
    isbn: str
    available_copies: int
    total_copies: int
    price: float
    publisher: Optional[str] = None
    published_date: date  # This will store the parsed date

    @field_validator('title')
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

    @field_validator('isbn')
    def validate_isbn(cls, v: str) -> str:
        pattern = r'^(97(8|9))?\d{9}(\d|X)$'
        if not re.match(pattern, v.replace("-", "")):
            raise ValueError("Invalid ISBN format")
        return v

    @field_validator('available_copies')
    def cant_be_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Available copies cannot be negative")
        return v

    @field_validator('price')
    def price_must_be_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    @field_validator("published_date", mode="before")
    def parse_and_validate_date(cls, v: str) -> date:
        try:
            return datetime.strptime(v, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Date must be in format DD-MM-YYYY (e.g., 29-07-2025)")

    @model_validator(mode="after")
    def check_copies_consistency(self) -> 'Book':
        if self.available_copies > self.total_copies:
            raise ValueError("Available copies cannot exceed total copies")
        return self


#  Dummy JSON Test (Valid Case)
valid_data = {
    "title": "Introduction to Python",
    "isbn": "9780135166307",
    "total_copies": 10,
    "available_copies": 5,
    "price": 599.99,
    "publisher": "Tech Books Inc",
    "published_date": "29-07-2025"
}

#  Dummy JSON Test (Invalid Case)
invalid_data = {
    "title": "  ",  # Empty title
    "isbn": "123456789",  # Invalid ISBN
    "total_copies": 3,
    "available_copies": 5,  # More than total
    "price": -200.0,  # Negative price
    "publisher": "Bad Books Co.",
    "published_date": "2025-07-29"  # Wrong format
}

logger.info("\nValid Book:")
try:
    book = Book(**valid_data)
    logger.info(book)
except Exception as e:
    logger.error("Validation error: %s", e)

logger.info("\nInvalid Book:")
try:
    book = Book(**invalid_data)
    logger.info(book)
except Exception as e:
    logger.error("Validation error: %s", e)

