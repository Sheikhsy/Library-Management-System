from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator

class Library(models.Model):
    class Meta:
        db_table = "Library1"
    library_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    campus_location = models.CharField(max_length=100)
    contact_email = models.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])
    phone_number = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Library name cannot be empty.")
        if not self.campus_location.strip():
            raise ValidationError("Campus location cannot be empty.")

    def save(self, *args, **kwargs):
        # Run full validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True,validators=[EmailValidator(message="Enter a valid email address.")])
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def clean(self):
        if not self.first_name.strip() or not self.last_name.strip():
            raise ValidationError("Author name cannot be blank.")
    def save(self, *args, **kwargs):
        # Run full validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def clean(self):
        if not self.name:
            raise ValidationError("Category name is required.")
    def __str__(self):
        return self.name if self.name else "Unnamed Category"

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    summary = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    authors = models.ManyToManyField(Author, blank=True)

    class Meta:
        ordering = ["book_id"]

    def clean(self):
        if self.available_copies > self.total_copies:
            raise ValidationError("Available copies cannot exceed total copies.")
    def save(self, *args, **kwargs):
        # Run full validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title



class Member(models.Model):
    MEMBER_TYPES = [
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
    ]

    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    member_type = models.CharField(max_length=10, choices=MEMBER_TYPES)
    registration_date = models.DateField()

    def clean(self):
        if not self.first_name.strip() or not self.last_name.strip():
            raise ValidationError("Member name cannot be empty.")
    def save(self, *args, **kwargs):
        # Run full validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_date = models.DateField()

    def save(self, *args, **kwargs):
        self.full_clean()  # runs all field and model validations
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Review for {self.book} by {self.member}"


class Borrowing(models.Model):
    borrowing_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    borrow_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    returned = models.BooleanField(default=False)

    def clean(self):
        if self.return_date and self.borrow_date and self.return_date < self.borrow_date:
            raise ValidationError("Return date cannot be before borrow date.")
    def save(self, *args, **kwargs):
        # Run full validation before saving
        self.full_clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.member} borrowed {self.book}"
