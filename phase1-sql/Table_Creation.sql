Populated tables with related sample records
Create Database lb_system;

Use lb_system;

show tables;


-- Library table
CREATE TABLE `Library` (
    library_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    campus_location VARCHAR(100),
    contact_email VARCHAR(100),
    phone_number VARCHAR(20)
);

select * from `Library`;

desc `Library`;


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

-- Author table
CREATE TABLE Author (
    author_id INT auto_increment PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE,
    nationality VARCHAR(100),
    biography TEXT
);

-- Category table
CREATE TABLE Category (
    category_id INT auto_increment PRIMARY KEY,
    name VARCHAR(100),
    description TEXT
);

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

-- BookAuthor (junction table)
CREATE TABLE BookAuthor (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id) on UPDATE CASCADE,
    FOREIGN KEY (author_id) REFERENCES Author(author_id) on UPDATE CASCADE
);

-- BookCategory (junction table)
CREATE TABLE BookCategory (
    book_id INT,
    category_id INT,
    PRIMARY KEY (book_id, category_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id) on UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Category(category_id) on UPDATE CASCADE
);