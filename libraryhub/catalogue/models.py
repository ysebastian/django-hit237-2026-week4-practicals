from django.contrib.auth.models import User
from django.db import models

from .managers import LoanManager


class Author(models.Model):
	name = models.CharField(max_length=200)
	date_of_birth = models.DateField(null=True, blank=True)
	biography = models.TextField(blank=True)
	nationality = models.CharField(max_length=100, default='Unknown')

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class Book(models.Model):
	title = models.CharField(max_length=300)
	isbn = models.CharField(max_length=13, unique=True)
	genre = models.CharField(max_length=100)
	publication_year = models.PositiveIntegerField()
	page_count = models.PositiveIntegerField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
	is_available = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.title} ({self.author.name})"

	class Meta:
		ordering = ['title']


class Member(models.Model):
	MEMBERSHIP_CHOICES = [
		('standard', 'Standard'),
		('premium', 'Premium'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
	library_card_number = models.CharField(max_length=20, unique=True)
	membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='standard')
	join_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} ({self.library_card_number})"

	class Meta:
		ordering = ['user__username']


class Loan(models.Model):
	STATUS_CHOICES = [
		('active', 'Active'),
		('returned', 'Returned'),
		('overdue', 'Overdue'),
	]

	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
	member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
	date_borrowed = models.DateField()
	date_due = models.DateField()
	date_returned = models.DateField(null=True, blank=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

	objects = LoanManager()

	def __str__(self):
		return f"Loan: {self.book.title} to {self.member.user.username}"

	class Meta:
		ordering = ['-date_borrowed']
