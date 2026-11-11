from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books')
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    @property
    def issued_copies(self):
        return self.total_copies - self.available_copies

class Member(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    student_id = models.CharField(max_length=50, unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.student_id})'

class Loan(models.Model):
    STATUS_CHOICES = [('ISSUED', 'Issued'), ('RETURNED', 'Returned')]
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='loans')
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='loans')
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    issue_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ISSUED')

    class Meta:
        ordering = ['-issue_date', '-id']

    def __str__(self):
        return f'{self.book.title} - {self.member.name}'

    @property
    def is_overdue(self):
        return self.status == 'ISSUED' and self.due_date < timezone.localdate()

    @property
    def fine(self):
        if self.status == 'RETURNED' and self.return_date:
            days = max((self.return_date - self.due_date).days, 0)
        elif self.status == 'ISSUED':
            days = max((timezone.localdate() - self.due_date).days, 0)
        else:
            days = 0
        return days * 2
