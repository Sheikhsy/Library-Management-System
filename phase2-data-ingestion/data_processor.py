import argparse
import csv
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, List, Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from model import Base, Library1, Book, Author, Member ,Borrowing, Review,Category
from schemas import Library1 as LibrarySchema, Book as BookSchema, Author as AuthorSchema, Member as MemberSchema
from schemas import Borrowing as BorrowingSchema , Review as ReviewSchema,Category as CategorySchema
from logging.handlers import RotatingFileHandler

# Logging
def configure_logging(level: str, log_path: str = "etl.log") -> None:
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)

    # Clear existing handlers (avoids duplicate logs if reconfigured)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter(log_format))

    # Rotating File Handler (DEBUG and above)
    file_handler = RotatingFileHandler(log_path, maxBytes=5_000_000, backupCount=2)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Apply configuration
    logging.basicConfig(
        level=logging.DEBUG,  # Root logger level
        handlers=[console_handler, file_handler]
    )

# CLI
def parse_cli():
    parser = argparse.ArgumentParser(description="Library ETL (CSV → MySQL)")
    parser.add_argument("-d", "--directory", required=True,
                        help="Folder with CSV files (libraries.csv, books.csv, ...)")
    parser.add_argument("--db", "--database-url", required=True,
                        help="SQLAlchemy DB url, e.g. mysql+pymysql://user:pass@host/db")
    parser.add_argument("--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return parser.parse_args()


# DB session
def get_session(db_url: str) -> Session:
    engine = create_engine(db_url, echo=False, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


# Generic CSV processor
def process_file(
    path: str,
    schema_cls,
    model_cls,
    session: Session,
    natural_key: str | None = None
) -> Tuple[int, int, int]:
    inserted = skipped = invalid = 0
    logger = logging.getLogger(model_cls.__name__)

    if not os.path.isfile(path):
        logger.warning("File %s not found – skipping", path)
        return 0, 0, 0

    with open(path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                clean = schema_cls(**{k.strip(): v for k, v in row.items()}).model_dump()

                # natural-key duplicate check
                if natural_key and clean.get(natural_key):
                    col = getattr(model_cls, natural_key)
                    if session.query(model_cls).filter(col == clean[natural_key]).first():
                        logger.debug("Duplicate %s=%s – skipping", natural_key, clean[natural_key])
                        skipped += 1
                        continue

                # date string → date object
                for df in ("publication_date", "birth_date", "registration_date"):
                    if df in clean and isinstance(clean[df], str):
                        clean[df] = datetime.strptime(clean[df], "%Y-%m-%d").date()

                # safe insert
                try:
                    session.add(model_cls(**clean))
                    session.flush()
                    inserted += 1
                except IntegrityError as e:
                    logger.warning("Skipping row: %s", e.orig)
                    session.rollback()   # only rolls back this row
                    invalid += 1

            except Exception as e:
                logger.warning("Invalid row %s: %s", row, e)
                invalid += 1

    session.commit()
    logger.info("Inserted=%d skipped=%d invalid=%d", inserted, skipped, invalid)
    return inserted, skipped, invalid


# Main
def main() -> None:
    args = parse_cli()
    configure_logging(args.log_level)
    session = get_session(args.db)
    summary: Dict[str, Tuple[int, int, int]] = {}


    summary["libraries"] = process_file(
        os.path.join(args.directory, "library.csv"),
        LibrarySchema, Library1, session, "contact_email"
    )

    summary["books"] = process_file(
        os.path.join(args.directory, "book.csv"),
        BookSchema, Book, session, "isbn"
    )

    summary["authors"] = process_file(
        os.path.join(args.directory, "author.csv"),
        AuthorSchema, Author, session, None   # no single natural key
    )

    summary["members"] = process_file(
        os.path.join(args.directory, "member.csv"),
        MemberSchema, Member, session, "email"
    )
    summary["borrowings"] = process_file(
        os.path.join(args.directory, "borrowing.csv"),
        BorrowingSchema, Borrowing, session, None
    )
    summary["reviews"] = process_file(
        os.path.join(args.directory, "review.csv"),
        ReviewSchema, Review, session, None
    )
    summary["categories"] = process_file(
        os.path.join(args.directory, "category.csv"),
        CategorySchema, Category, session, None
    )
    session.close()
    logging.info("=== ETL SUMMARY ===")
    for entity, (ins, sk, inv) in summary.items():
        logging.info("%-10s : inserted=%-3d skipped=%-3d invalid=%-3d", entity, ins, sk, inv)


if __name__ == "__main__":
    main()