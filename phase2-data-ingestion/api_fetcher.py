import argparse
from api_client import OpenLibraryAPIClient
from model import Author, Book, BookAuthor
from schemas import Author as AuthorSchema, Book as BookSchema
from datetime import datetime
from typing import Optional
from settings import get_session


from settings import configure_logging
import logging

configure_logging()
logger = logging.getLogger(__name__)


def parse_author_name(full_name: str):
    parts = full_name.strip().split()
    first_name = parts[0]
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
    return first_name, last_name

def parse_date(date_str: Optional[str]) -> Optional[datetime.date]:
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y", "%B %d, %Y", "%d %B %Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

def map_author_data(raw_author: dict, full_name: str) -> Optional[AuthorSchema]:
    first_name, last_name = parse_author_name(full_name)
    return AuthorSchema(
        first_name=first_name,
        last_name=last_name,
        birth_date=parse_date(raw_author.get("birth_date")),
        email=None,
        phone_number=None,
        nationality=raw_author.get("nationality", "Unknown"),
        biography=raw_author.get("bio") if isinstance(raw_author.get("bio"), str)
            else raw_author.get("bio", {}).get("value", None)
    )

def map_book_data(raw_book: dict) -> Optional[BookSchema]:
    title = raw_book.get("title")
    isbn = None
    if "isbn" in raw_book:
        isbn_list = raw_book.get("isbn")
        if isinstance(isbn_list, list):
            isbn = isbn_list[0]

    return BookSchema(
        library_id=1,
        title=title,
        isbn=isbn,
        publication_date=parse_date(raw_book.get("first_publish_year")),
        total_copies=5,
        available_copies=5
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True, help="Author name (e.g., 'Charles Dickens')")
    parser.add_argument("--limit", type=int, default=10, help="Limit number of books to fetch.")
    parser.add_argument("--db", "--db-url", dest="db_url", required=True, help="Database URL")
    args = parser.parse_args()

    client = OpenLibraryAPIClient()
    session = get_session(args.db_url)

    logger.info(f"Searching for author: {args.author}")
    search_result = client.get("/search/authors.json", params={"q": args.author})

    if not search_result.get("docs"):
        logger.error(f"No author found with name: {args.author}")
        return

    author_doc = search_result["docs"][0]
    author_key = author_doc.get("key")
    if not author_key:
        logger.error("Author key not found.")
        return

    author_id = author_key.split("/")[-1]
    raw_author = client.get(f"/authors/{author_id}.json")
    author_schema = map_author_data(raw_author, args.author)

    if not author_schema:
        logger.error("Author schema validation failed.")
        return

    author = Author(**author_schema.model_dump())
    session.add(author)
    session.commit()
    logger.info(f"Saved author: {author.first_name} {author.last_name} (ID: {author.author_id})")

    works_data = client.get(f"/authors/{author_id}/works.json", params={"limit": args.limit})
    works = works_data.get("entries", [])
    logger.info(f"Found {len(works)} books for author.")

    for work in works:
        book_schema = map_book_data(work)
        if book_schema:
            book = Book(**book_schema.model_dump())
            session.add(book)
            session.commit()
            logger.info(f"Saved book: {book.title} (ID: {book.book_id})")

            book_author = BookAuthor(author_id=author.author_id, book_id=book.book_id)
            session.add(book_author)
            session.commit()
            logger.info(f"Linked book '{book.title}' to author '{author.first_name} {author.last_name}'")

if __name__ == "__main__":
    main()
