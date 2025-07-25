-- 1.Excercise:
-- Books with their authors and categories

SELECT 
  b.title AS Book_Title,
  GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS Authors,
  GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS Categories
FROM Book b
JOIN BookAuthor ba ON b.book_id = ba.book_id
JOIN Author a ON ba.author_id = a.author_id
JOIN BookCategory bc ON b.book_id = bc.book_id
JOIN Category c ON bc.category_id = c.category_id
GROUP BY b.book_id, b.title;



-- Most borrowed books in the last 30 days

WITH cte AS (
  SELECT 
    b.title AS Title,
    COUNT(br.borrowing_id) AS Borrowed_Times
  FROM Borrowing br
  JOIN Book b ON br.book_id = b.book_id
  WHERE br.borrow_date >= CURDATE() - INTERVAL 30 DAY
  GROUP BY b.title
)
SELECT 
  Title,
  Borrowed_Times
FROM cte
ORDER BY Borrowed_Times DESC;

-- Members with overdue books and calculated late fees
SELECT 
  CONCAT(m.first_name, ' ', m.last_name),
  SUM(br.late_fee) AS Late_Fee
FROM member m 
JOIN borrowing br ON m.member_id = br.member_id 
WHERE br.return_date > br.due_date
GROUP BY m.member_id;


-- Average rating per book with author information
SELECT b.title as Title, AVG(re.rating) AS Avg_Rating,
group_concat( concat(a.first_name,' ', a.last_name) SEPARATOR ', ')as Authors
FROM Review re JOIN Book b ON re.book_id = b.book_id 
JOIN bookauthor ba ON re.book_id=ba.book_id
JOIN author a ON ba.author_id=a.author_id
GROUP BY b.title order by Avg_Rating DESC;



-- Books available in each library with stock levels

desc Book;
With Details as (
SELECT 
  l.name AS Library_Name,
  COUNT(b.book_id) AS Total_Book_Titles,
  SUM(b.total_copies) AS Total_Copies,
  SUM(b.available_copies) AS Available_Copies
FROM Book b
JOIN `Library` l ON b.library_id = l.library_id
GROUP BY l.library_id
ORDER BY l.name),
CTE as(
Select Library_Name,Total_Book_Titles,Total_Copies,Available_Copies,
FLOOR((available_copies / total_copies) * 100) AS Availability_Percentage
from details
)
Select Library_Name,Total_Book_Titles,Total_Copies,Available_Copies,Availability_Percentage,

CASE WHEN Available_Copies = 0 THEN "Out of Stock"
WHEN Available_Copies = Total_Copies THEN "Full Stock"
WHEN Availability_Percentage<0.4 THEN "Low Stock"
ELSE "Enough Stock"
END as Stock_Level from CTE
;



-- BOOK ANALYSIS

-- 1.Common Books that are found in all libraries and total copies of them available

SELECT b.title, SUM(b.available_copies) AS Total_Copies_Available
FROM book b
GROUP BY b.title
HAVING COUNT(DISTINCT b.library_id) = 3;

-- 2.Books that got borrowed most in order (Hot Items)

with cte as (
select b.title as Title, sum(b.total_copies) as Total, sum(b.available_copies) as Available
from book b group by b.title)
select Title, Total - Available as Borrowed_Times, Available 
from cte order by Borrowed_Times;

-- 3. Total Books by Author
Select a.first_name,a.last_name, count(b.title) as Number_of_books
from author a 
JOIN bookauthor ba ON a.author_id=ba.author_id
JOIN book b ON b.book_id=ba.book_id 

group by a.author_id order by Number_of_books DESC;

-- 4. Members that borowwed more than average (Active Member) 
WITH mem_total AS (
  SELECT member_id, COUNT(borrowing_id) AS Borrowed
  FROM borrowing
  GROUP BY member_id
),
borrow_stats AS (
  SELECT 
    COUNT(borrowing_id) AS Total_Borrow,
    COUNT(DISTINCT member_id) AS Total_Borrower
  FROM borrowing
),
avg_stats AS (
  SELECT 
    Total_Borrow, 
    Total_Borrower,
    FLOOR(Total_Borrow / Total_Borrower) AS Average_Borrow
  FROM borrow_stats
)
SELECT m.member_id
FROM mem_total m
JOIN avg_stats a
  ON m.Borrowed > a.Average_Borrow;


# 5.Reduce the avaialabilty by 2 for book_id =1 if it's negative Roll Back

-- Start a transaction
START TRANSACTION;

-- Check the current available copies for Book ID 1
SELECT title, available_copies FROM Book WHERE book_id = 1;

-- Reduce available copies 
UPDATE Book SET available_copies = available_copies - 2 WHERE book_id = 1;

--  Check if update is valid
SELECT available_copies FROM Book WHERE book_id = 1;

-- If available_copies >= 0, commit the transaction
-- Else, rollback
ROLLBACK;

