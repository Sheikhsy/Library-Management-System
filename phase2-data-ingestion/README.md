# Phase 2: Data Ingestion (Python ETL)

## Overview
In this phase, you will develop Python scripts to ingest, transform, and load data into the Library Management System database. You'll learn about ETL (Extract, Transform, Load) processes, data validation, and Python best practices.

## Learning Objectives
- Understand ETL processes and their importance in data management
- Develop Python scripts to handle data ingestion from various sources
- Implement data validation and error handling
- Apply Python best practices for maintainable and efficient code

## Tasks

## Task 1: CSV Data Processing and Database Insertion

### Objective
Create a Python script that processes noisy CSV files containing library data, validates and cleans the data, then inserts it into a database.

### Requirements

#### Command Line Interface
Your script must accept the following command line arguments:
- `--directory` or `-d`: Path to directory containing CSV files
- `--database-url` or `--db`: Database connection URL
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `--help`: Display help information

Example usage:
```shell
python data_processor.py --directory ./csv_data --db postgresql://user:pass@localhost/library --log-level INFO
```
#### CSV Files to Process
The directory will contain these noisy CSV files:
1. `libraries.csv` - Library information with duplicate entries, invalid emails, malformed phone numbers
2. `books.csv` - Book data with invalid ISBNs, missing dates, inconsistent formatting
3. `authors.csv` - Author information with name variations, invalid birth dates, missing data
4. `members.csv` - Member data with invalid emails, phone numbers, duplicate entries

#### Data Validation and Normalization
Use **Pydantic** schemas to validate and clean:

**ISBN Validation:**
- Validate ISBN-10 and ISBN-13 formats
- Remove hyphens and spaces
- Verify check digits

**Email Validation:**
- Use Pydantic's EmailStr type
- Handle malformed email addresses gracefully

**Name Normalization:**
- Standardize name capitalization (Title Case)
- Handle multiple name variations for the same person
- Trim whitespace

**Phone Number Normalization:**
- Extract digits only
- Format to standard pattern (e.g., +1-XXX-XXX-XXXX)
- Handle international formats

#### Database Operations
- Use **SQLAlchemy ORM** to define models and handle database operations
- Implement proper transaction management
- Handle duplicate detection and prevention
- Create appropriate indexes for performance

#### Error Handling and Logging
- Implement comprehensive logging using Python's logging module
- Log validation errors, skipped records, and processing statistics
- Use try-catch blocks for database operations
- Generate a summary report of processed records

### Deliverables
- `data_processor.py` - Main script with command line interface
- `models.py` - SQLAlchemy models
- `schemas.py` - Pydantic validation schemas
- `requirements.txt` or `pyproject.toml` - Project dependencies
- `README.md` - Setup and usage instructions


## Task 2: External API Data Integration

### Objective
Create a Python script that fetches book data from the Open Library API for your favorite author, validates the data, and stores it in the database.

### API Reference
**Open Library API:**
- Base URL: `https://openlibrary.org`
- Author Search: `/search/authors.json?q={author_name}`
- Author Works: `/authors/{author_key}/works.json`
- Book Details: `/works/{work_key}.json`
- Documentation: https://openlibrary.org/developers/api
- No authentication required

### Requirements

#### Command Line Interface
```shell
python api_fetcher.py --author "Charles Dickens" --limit 20 --db <db_connection_url>
```
Arguments:
- `--author`: Author name to search for
- `--limit`: Maximum number of books to fetch
- `--database-url` or `--db`: Database connection URL
- `--output`: Optional JSON file to save raw API responses

#### API Integration Tasks
1. **Author Search**: Find the author using the search endpoint
2. **Fetch Works**: Get the author's works (books)
3. **Book Details**: Fetch detailed information for each book
4. **Rate Limiting**: Implement respectful API usage (1 request per second)
5. **Error Handling**: Handle API failures, timeouts, and missing data

#### Data Processing
- Use the same Pydantic schemas from Task 1 for validation
- Handle missing or incomplete data from API responses
- Map API response fields to your database schema
- Avoid duplicate entries (check ISBN or title/author combination)

### Deliverables
- `api_fetcher.py` - Main script with API integration
- `api_client.py` - Reusable API client class
- Enhanced models and schemas if needed

## Resources
- [Python Documentation](https://docs.python.org/3/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Requests Library](https://requests.readthedocs.io/en/latest/)
- [JSON in Python](https://docs.python.org/3/library/json.html)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Open Library API Documentation](https://openlibrary.org/developers/api)
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Argparse Tutorial](https://docs.python.org/3/tutorial/stdlib.html#command-line-arguments)
