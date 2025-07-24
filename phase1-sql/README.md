# Phase 1: Database Design & SQL Implementation

## Overview
In this phase, you will design and implement the database schema for the Library Management System. You'll learn about entity relationships, SQL schema definition, and complex query operations.

## Learning Objectives
- Understand and implement various types of database relationships
- Create a well-structured database schema with appropriate constraints
- Write complex SQL queries to retrieve and manipulate data
- Apply database design best practices

## Tasks

### Task 1: Entity Relationship Diagram (ERD)

Create an Entity Relationship Diagram that includes the following entities and relationships:

#### Entities:
1. **Library** (One-to-Many with Books)
   - Attributes: library_id, name, campus_location, contact_email, phone_number

2. **Book** (Many-to-Many with Authors, Many-to-Many with Categories)
   - Attributes: book_id, title, isbn, publication_date, total_copies, available_copies, library_id

3. **Author** (Many-to-Many with Books)
   - Attributes: author_id, first_name, last_name, birth_date, nationality, biography

4. **Category** (Many-to-Many with Books)
   - Attributes: category_id, name, description

5. **Member** (One-to-Many with Borrowings, One-to-Many with Reviews)
   - Attributes: member_id, first_name, last_name, email, phone, member_type (student/faculty), registration_date

6. **Borrowing** (Many-to-One with Member, Many-to-One with Book)
   - Attributes: borrowing_id, member_id, book_id, borrow_date, due_date, return_date, late_fee

7. **Review** (Many-to-One with Member, Many-to-One with Book)
   - Attributes: review_id, member_id, book_id, rating (1-5), comment, review_date

8. **BookAuthor** (Junction table for Many-to-Many)
   - Attributes: book_id, author_id

9. **BookCategory** (Junction table for Many-to-Many)
   - Attributes: book_id, category_id

#### Relationship Requirements:
- **One-to-Many**: Library → Books, Member → Borrowings, Member → Reviews
- **Many-to-Many**: Books ↔ Authors, Books ↔ Categories  
- **One-to-One**: Member + Book → Review (a member can only review a book once)

**Deliverable:** ERD diagram using draw.io, Lucidchart, or similar tool

### Task 2: SQL Schema Definition (DDL)

Create SQL DDL statements to define the database schema based on your ERD.

**Requirements:**
- All tables must have primary keys
- Implement all foreign key constraints
- Include CHECK constraints where applicable (e.g., rating between 1-5)
- Add UNIQUE constraints where needed
- Include created_at and updated_at timestamp fields

**Deliverable:** Complete DDL script file (`schema.sql`)

### Task 3: Sample Data & DML Operations

Create DML statements for:

1. **Insert Operations:**
   - 3 libraries
   - 15 books distributed across libraries
   - 8 authors
   - 5 categories
   - 20 members (mix of students and faculty)
   - 25 borrowing records
   - 12 reviews

2. **Complex Query Operations:**
   Write queries to demonstrate:
   - JOIN operations across multiple tables
   - Aggregation functions (COUNT, AVG, SUM)
   - Subqueries and Common Table Expressions (CTEs)
   - Window functions
   - Transaction management

**Deliverable:** DML script file (`data.sql`) and a query file (`queries.sql`)

**Example Required Queries:**
```sql
-- Books with their authors and categories
-- Most borrowed books in the last 30 days
-- Members with overdue books and calculated late fees
-- Average rating per book with author information
-- Books available in each library with stock levels
```

## Evaluation Criteria
- Correct implementation of entity relationships
- Proper use of constraints and indexes
- Efficiency and correctness of SQL queries
- Adherence to SQL best practices
- Completeness of the solution

## Resources
- [Database Design Tutorial](https://www.lucidchart.com/pages/database-diagram/database-design)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [Entity Relationship Diagram Guide](https://www.visual-paradigm.com/guide/data-modeling/what-is-entity-relationship-diagram/)