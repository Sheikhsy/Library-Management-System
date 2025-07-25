INSERT INTO `Library` (name, campus_location, contact_email, phone_number)
VALUES 
('Central Library', 'Main Campus', 'central@univ.edu', '9876543210'),
('Science Library', 'North Campus', 'science@univ.edu', '9876543211'),
('Arts Library', 'South Campus', 'arts@univ.edu', '9876543212');


INSERT INTO Author (first_name, last_name, birth_date, nationality, biography)
VALUES 
('John', 'Doe', '1975-05-14', 'American', 'Expert in literature.'),
('Alice', 'Smith', '1980-09-22', 'British', 'Known for science fiction.'),
('Robert', 'Brown', '1965-11-30', 'Canadian', 'Writes on data science.'),
('Maria', 'Garcia', '1978-07-19', 'Spanish', 'Children\'s book author.'),
('David', 'Lee', '1982-03-10', 'Australian', 'Popular fiction writer.'),
('Emma', 'Wilson', '1990-06-05', 'British', 'Writes historical novels.'),
('Daniel', 'Taylor', '1988-01-25', 'American', 'AI researcher turned writer.'),
('Sophie', 'Chen', '1992-10-17', 'Chinese', 'Writes technical manuals.');


INSERT INTO Category (name, description)
VALUES 
('Fiction', 'Imaginative narrative works.'),
('Science', 'Scientific and research content.'),
('History', 'Historical analysis and events.'),
('Children', 'Books for children and young readers.'),
('Technology', 'Books on technology and computing.');


INSERT INTO Book (title, isbn, publication_date, total_copies, available_copies, library_id)
VALUES 
('The Future Code', '978-1234567890', '2020-03-15', 5, 3, 1),
('Quantum Leap', '978-0987654321', '2019-06-20', 4, 2, 1),
('Historical Echoes', '978-1122334455', '2018-09-10', 6, 4, 2),
('Child Wonders', '978-2233445566', '2021-01-05', 3, 1, 3),
('Machine Mind', '978-3344556677', '2022-07-22', 7, 6, 1),
('Tales of Earth', '978-4455667788', '2017-11-13', 4, 2, 2),
('Python for All', '978-5566778899', '2023-02-01', 8, 5, 1),
('Fantasy Island', '978-6677889900', '2016-04-18', 2, 1, 3),
('Robotics Age', '978-7788990011', '2022-10-10', 6, 3, 2),
('History Rewritten', '978-8899001122', '2021-08-08', 5, 2, 2),
('AI Revolution', '978-9900112233', '2023-05-15', 10, 7, 1),
('Ocean of Dreams', '978-1011121314', '2020-12-01', 3, 1, 3),
('Fairy Forest', '978-1213141516', '2019-03-07', 4, 2, 3),
('Microchip World', '978-1415161718', '2021-11-11', 5, 4, 2),
('The Lost Empire', '978-1617181920', '2020-05-30', 6, 3, 1);



INSERT INTO BookAuthor (book_id, author_id)
VALUES 
(1, 1), (1, 7),
(2, 2),
(3, 6),
(4, 4),
(5, 3), (5, 7),
(6, 1),
(7, 3),
(8, 5),
(9, 3), (9, 7),
(10, 6),
(11, 7), (11, 8),
(12, 5),
(13, 4),
(14, 8),
(15, 2);

INSERT INTO BookCategory (book_id, category_id)
VALUES 
(1, 5), (1, 2),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 1),
(7, 5),
(8, 1),
(9, 5),
(10, 3),
(11, 5), (11, 2),
(12, 1),
(13, 4),
(14, 5),
(15, 3);


INSERT INTO Member (first_name, last_name, email, phone, member_type, registration_date)
VALUES 
('Arjun', 'Patel', 'arjun.patel@example.com', '9876000001', 'student', '2023-01-15'),
('Neha', 'Sharma', 'neha.sharma@example.com', '9876000002', 'faculty', '2022-12-10'),
('Ravi', 'Kumar', 'ravi.kumar@example.com', '9876000003', 'student', '2023-03-18'),
('Sneha', 'Rao', 'sneha.rao@example.com', '9876000004', 'faculty', '2021-07-22'),
('Amit', 'Verma', 'amit.verma@example.com', '9876000005', 'student', '2023-02-14'),
('Priya', 'Das', 'priya.das@example.com', '9876000006', 'faculty', '2022-08-19'),
('Karan', 'Mehta', 'karan.mehta@example.com', '9876000007', 'student', '2023-04-01'),
('Tanvi', 'Singh', 'tanvi.singh@example.com', '9876000008', 'student', '2023-05-09'),
('Raj', 'Kapoor', 'raj.kapoor@example.com', '9876000009', 'faculty', '2022-11-11'),
('Divya', 'Mishra', 'divya.mishra@example.com', '9876000010', 'student', '2023-06-21'),
('Soham', 'Bose', 'soham.bose@example.com', '9876000011', 'student', '2023-01-03'),
('Isha', 'Gupta', 'isha.gupta@example.com', '9876000012', 'faculty', '2021-09-14'),
('Manav', 'Sen', 'manav.sen@example.com', '9876000013', 'student', '2023-06-30'),
('Rekha', 'Chatterjee', 'rekha.chatterjee@example.com', '9876000014', 'faculty', '2022-05-18'),
('Tanya', 'Roy', 'tanya.roy@example.com', '9876000015', 'student', '2023-03-20'),
('Vikram', 'Nair', 'vikram.nair@example.com', '9876000016', 'faculty', '2021-06-06'),
('Anjali', 'Jain', 'anjali.jain@example.com', '9876000017', 'student', '2023-02-28'),
('Ritika', 'Sen', 'ritika.sen@example.com', '9876000018', 'faculty', '2021-08-12'),
('Shivam', 'Mitra', 'shivam.mitra@example.com', '9876000019', 'student', '2023-01-22'),
('Kavya', 'Saxena', 'kavya.saxena@example.com', '9876000020', 'faculty', '2022-04-03');


INSERT INTO Borrowing (member_id, book_id, borrow_date, due_date, return_date, late_fee)
VALUES 
(1, 1, '2023-06-01', '2023-06-15', '2023-06-14', 0.00),
(2, 2, '2023-06-03', '2023-06-17', '2023-06-20', 15.00),
(3, 3, '2023-06-05', '2023-06-19', NULL, 0.00),
(4, 4, '2023-06-07', '2023-06-21', '2023-06-20', 0.00),
(5, 5, '2023-06-09', '2023-06-23', '2023-06-24', 10.00),
(6, 6, '2023-06-10', '2023-06-24', NULL, 0.00),
(7, 7, '2023-06-11', '2023-06-25', '2023-06-25', 0.00),
(8, 8, '2023-06-12', '2023-06-26', '2023-06-27', 5.00),
(9, 9, '2023-06-13', '2023-06-27', NULL, 0.00),
(10, 10, '2023-06-14', '2023-06-28', NULL, 0.00),
(11, 11, '2023-06-15', '2023-06-29', '2023-06-30', 5.00),
(12, 12, '2023-06-16', '2023-06-30', NULL, 0.00),
(13, 13, '2023-06-17', '2023-07-01', '2023-07-01', 0.00),
(14, 14, '2023-06-18', '2023-07-02', '2023-07-04', 10.00),
(15, 15, '2023-06-19', '2023-07-03', NULL, 0.00),
(16, 1, '2023-06-20', '2023-07-04', NULL, 0.00),
(17, 2, '2023-06-21', '2023-07-05', NULL, 0.00),
(18, 3, '2023-06-22', '2023-07-06', NULL, 0.00),
(19, 4, '2023-06-23', '2023-07-07', NULL, 0.00),
(20, 5, '2023-06-24', '2023-07-08', NULL, 0.00),
(1, 6, '2023-06-25', '2023-07-09', NULL, 0.00),
(2, 7, '2023-06-26', '2023-07-10', NULL, 0.00),
(3, 8, '2023-06-27', '2023-07-11', NULL, 0.00),
(4, 9, '2023-06-28', '2023-07-12', NULL, 0.00),
(5, 10, '2023-06-29', '2023-07-13', NULL, 0.00);

INSERT INTO Review (member_id, book_id, rating, comment, review_date)
VALUES 
(1, 1, 5, 'Great insights on AI.', '2023-06-16'),
(2, 2, 4, 'Well-written.', '2023-06-18'),
(3, 3, 3, 'A bit too long.', '2023-06-20'),
(4, 4, 5, 'My kids loved it.', '2023-06-22'),
(5, 5, 2, 'Too technical.', '2023-06-24'),
(6, 6, 4, 'Enjoyed the journey.', '2023-06-26'),
(7, 7, 3, 'Good for beginners.', '2023-06-28'),
(8, 8, 4, 'Imaginative.', '2023-06-30'),
(9, 9, 5, 'Cutting-edge info.', '2023-07-01'),
(10, 10, 3, 'Neutral read.', '2023-07-02'),
(11, 11, 4, 'Forward-thinking.', '2023-07-03'),
(12, 12, 5, 'A dreamscape!', '2023-07-04');