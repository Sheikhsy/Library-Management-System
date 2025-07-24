Create Database lb_system;

Use lb_system;













show tables;


/*Library (One-to-Many with Books)

Attributes: library_id, name, campus_location, contact_email, phone_number*/


-- Library table
CREATE TABLE `Library` (
    library_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    campus_location VARCHAR(100),
    contact_email VARCHAR(100),
    phone_number VARCHAR(20)
);
DROP TABLE IF EXISTS Library;
select * from `Library`;

desc `Library`;

/*Book (Many-to-Many with Authors, Many-to-Many with Categories)

Attributes: book_id, title, isbn, publication_date, total_copies, available_copies, library_id*/

-- Book table
CREATE TABLE Book (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    isbn VARCHAR(20) UNIQUE,
    publication_date DATE,
    total_copies INT,
    available_copies INT,
    library_id INT,
    FOREIGN KEY (library_id) REFERENCES `Library`(library_id) on UPDATE CASCADE
);
/*Author (Many-to-Many with Books)

Attributes: author_id, first_name, last_name, birth_date, nationality, biography*/

-- Author table
CREATE TABLE Author (
    author_id INT auto_increment PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE,
    nationality VARCHAR(100),
    biography TEXT
);
/*Category (Many-to-Many with Books)

Attributes: category_id, name, description*/

-- Category table
CREATE TABLE Category (
    category_id INT auto_increment PRIMARY KEY,
    name VARCHAR(100),
    description TEXT
);
/*Member (One-to-Many with Borrowings, One-to-Many with Reviews)

Attributes: member_id, first_name, last_name, email, phone, member_type (student/faculty), registration_date
*/

-- Member table
CREATE TABLE Member (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    member_type ENUM('student', 'faculty') NOT NULL,
    registration_date DATE
);
/* Borrowing (Many-to-One with Member, Many-to-One with Book)
Attributes: borrowing_id, member_id, book_id, borrow_date, due_date, return_date, late_fee */

-- Borrowing table
CREATE TABLE Borrowing (
    borrowing_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    book_id INT,
    borrow_date DATE,
    due_date DATE,
    return_date DATE,
    late_fee DECIMAL(10, 2),
    FOREIGN KEY (member_id) REFERENCES Member(member_id) on UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Book(book_id) on UPDATE CASCADE
);

/*Review (Many-to-One with Member, Many-to-One with Book)

Attributes: review_id, member_id, book_id, rating (1-5), comment, review_date*/

-- Review table
CREATE TABLE Review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    book_id INT,
    rating INT CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date DATE,
    FOREIGN KEY (member_id) REFERENCES Member(member_id) on UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Book(book_id) on UPDATE CASCADE
);

/* BookAuthor (Junction table for Many-to-Many)

Attributes: book_id, author_id*/

-- BookAuthor (junction table)
CREATE TABLE BookAuthor (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id) on UPDATE CASCADE,
    FOREIGN KEY (author_id) REFERENCES Author(author_id) on UPDATE CASCADE
);

/*BookCategory (Junction table for Many-to-Many)

Attributes: book_id, category_id*/

-- BookCategory (junction table)
CREATE TABLE BookCategory (
    book_id INT,
    category_id INT,
    PRIMARY KEY (book_id, category_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id) on UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Category(category_id) on UPDATE CASCADE
);

