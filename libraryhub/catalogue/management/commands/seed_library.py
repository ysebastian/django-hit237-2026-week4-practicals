import random
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from catalogue.models import Author, Book, Loan, Member


class Command(BaseCommand):
    help = 'Seeds the database with sample library data.'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        Loan.objects.all().delete()
        Member.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        Book.objects.all().delete()
        Author.objects.all().delete()

        # ── Authors ────────────────────────────────────────────────────────────
        authors_data = [
            {'name': 'Frank Herbert',           'nationality': 'American',  'date_of_birth': date(1920, 10, 8)},
            {'name': 'Ursula K. Le Guin',        'nationality': 'American',  'date_of_birth': date(1929, 10, 21)},
            {'name': 'Agatha Christie',           'nationality': 'British',   'date_of_birth': date(1890, 9, 15)},
            {'name': 'George Orwell',             'nationality': 'British',   'date_of_birth': date(1903, 6, 25)},
            {'name': 'Toni Morrison',             'nationality': 'American',  'date_of_birth': date(1931, 2, 18)},
            {'name': 'Gabriel Garcia Marquez',    'nationality': 'Colombian', 'date_of_birth': date(1927, 3, 6)},
            {'name': 'Isaac Asimov',              'nationality': 'American',  'date_of_birth': date(1920, 1, 2)},
            {'name': 'J.R.R. Tolkien',            'nationality': 'British',   'date_of_birth': date(1892, 1, 3)},
        ]
        authors = [Author.objects.create(**a) for a in authors_data]
        herbert, leguin, christie, orwell, morrison, marquez, asimov, tolkien = authors

        # ── Books ──────────────────────────────────────────────────────────────
        books_data = [
            # Science Fiction
            {'title': 'Dune',                          'isbn': '9780441013593', 'genre': 'Science Fiction', 'publication_year': 1965, 'page_count': 412, 'author': herbert},
            {'title': 'Dune Messiah',                  'isbn': '9780441017585', 'genre': 'Science Fiction', 'publication_year': 1969, 'page_count': 226, 'author': herbert},
            {'title': 'The Left Hand of Darkness',     'isbn': '9780441478125', 'genre': 'Science Fiction', 'publication_year': 1969, 'page_count': 304, 'author': leguin},
            {'title': 'The Dispossessed',              'isbn': '9780061054815', 'genre': 'Science Fiction', 'publication_year': 1974, 'page_count': 387, 'author': leguin},
            {'title': 'Foundation',                    'isbn': '9780553293357', 'genre': 'Science Fiction', 'publication_year': 1951, 'page_count': 255, 'author': asimov},
            {'title': 'I, Robot',                      'isbn': '9780553294385', 'genre': 'Science Fiction', 'publication_year': 1950, 'page_count': 224, 'author': asimov},
            {'title': 'Foundation and Empire',         'isbn': '9780553293371', 'genre': 'Science Fiction', 'publication_year': 1952, 'page_count': 247, 'author': asimov},
            # Mystery
            {'title': 'Murder on the Orient Express',  'isbn': '9780007119318', 'genre': 'Mystery',         'publication_year': 1934, 'page_count': 256, 'author': christie},
            {'title': 'And Then There Were None',      'isbn': '9780007136834', 'genre': 'Mystery',         'publication_year': 1939, 'page_count': 224, 'author': christie},
            {'title': 'The ABC Murders',               'isbn': '9780007107650', 'genre': 'Mystery',         'publication_year': 1936, 'page_count': 256, 'author': christie},
            # Fiction
            {'title': '1984',                          'isbn': '9780451524935', 'genre': 'Fiction',         'publication_year': 1949, 'page_count': 328, 'author': orwell},
            {'title': 'Animal Farm',                   'isbn': '9780451526342', 'genre': 'Fiction',         'publication_year': 1945, 'page_count': 152, 'author': orwell},
            {'title': 'Beloved',                       'isbn': '9781400033416', 'genre': 'Fiction',         'publication_year': 1987, 'page_count': 321, 'author': morrison},
            {'title': 'The Bluest Eye',                'isbn': '9780307278449', 'genre': 'Fiction',         'publication_year': 1970, 'page_count': 206, 'author': morrison},
            {'title': 'One Hundred Years of Solitude', 'isbn': '9780060883287', 'genre': 'Fiction',         'publication_year': 1967, 'page_count': 417, 'author': marquez},
            {'title': 'Love in the Time of Cholera',   'isbn': '9780307389732', 'genre': 'Fiction',         'publication_year': 1985, 'page_count': 348, 'author': marquez},
            # Fantasy
            {'title': 'The Hobbit',                    'isbn': '9780547928227', 'genre': 'Fantasy',         'publication_year': 1937, 'page_count': 310, 'author': tolkien},
            {'title': 'The Fellowship of the Ring',    'isbn': '9780547928210', 'genre': 'Fantasy',         'publication_year': 1954, 'page_count': 479, 'author': tolkien},
            {'title': 'The Two Towers',                'isbn': '9780547928203', 'genre': 'Fantasy',         'publication_year': 1954, 'page_count': 415, 'author': tolkien},
            {'title': 'The Return of the King',        'isbn': '9780547928197', 'genre': 'Fantasy',         'publication_year': 1955, 'page_count': 544, 'author': tolkien},
            # Non-Fiction
            {'title': 'Homage to Catalonia',           'isbn': '9780156421171', 'genre': 'Non-Fiction',     'publication_year': 1938, 'page_count': 232, 'author': orwell},
        ]
        books = [Book.objects.create(**b) for b in books_data]

        # ── Users & Members ────────────────────────────────────────────────────
        users_data = [
            {'username': 'jsmith',    'first_name': 'John',    'last_name': 'Smith',    'email': 'jsmith@example.com',    'is_staff': False, 'card': 'LIB-0001', 'type': 'standard'},
            {'username': 'mjohnson',  'first_name': 'Mary',    'last_name': 'Johnson',  'email': 'mjohnson@example.com',  'is_staff': False, 'card': 'LIB-0002', 'type': 'standard'},
            {'username': 'abrown',    'first_name': 'Alice',   'last_name': 'Brown',    'email': 'abrown@example.com',    'is_staff': False, 'card': 'LIB-0003', 'type': 'premium'},
            {'username': 'ewilliams', 'first_name': 'Edward',  'last_name': 'Williams', 'email': 'ewilliams@example.com', 'is_staff': False, 'card': 'LIB-0004', 'type': 'premium'},
            {'username': 'rdavis',    'first_name': 'Rachel',  'last_name': 'Davis',    'email': 'rdavis@example.com',    'is_staff': False, 'card': 'LIB-0005', 'type': 'standard'},
            {'username': 'lmiller',   'first_name': 'Laura',   'last_name': 'Miller',   'email': 'lmiller@example.com',   'is_staff': False, 'card': 'LIB-0006', 'type': 'standard'},
            {'username': 'cwilson',   'first_name': 'Charles', 'last_name': 'Wilson',   'email': 'cwilson@example.com',   'is_staff': True,  'card': 'LIB-0007', 'type': 'standard'},
            {'username': 'kmoore',    'first_name': 'Karen',   'last_name': 'Moore',    'email': 'kmoore@example.com',    'is_staff': False, 'card': 'LIB-0008', 'type': 'standard'},
            {'username': 'ptaylor',   'first_name': 'Peter',   'last_name': 'Taylor',   'email': 'ptaylor@example.com',   'is_staff': True,  'card': 'LIB-0009', 'type': 'standard'},
            {'username': 'sthomas',   'first_name': 'Susan',   'last_name': 'Thomas',   'email': 'sthomas@example.com',   'is_staff': False, 'card': 'LIB-0010', 'type': 'standard'},
        ]
        members = []
        for ud in users_data:
            user = User.objects.create_user(
                username=ud['username'],
                first_name=ud['first_name'],
                last_name=ud['last_name'],
                email=ud['email'],
                password='password123',
                is_staff=ud['is_staff'],
            )
            member = Member.objects.create(
                user=user,
                library_card_number=ud['card'],
                membership_type=ud['type'],
            )
            members.append(member)

        # ── Loans ──────────────────────────────────────────────────────────────
        today = date.today()

        # Active loans: books[0:10] become unavailable
        for i in range(10):
            book = books[i]
            book.is_available = False
            book.save()
            Loan.objects.create(
                book=book,
                member=members[i % len(members)],
                date_borrowed=today - timedelta(days=random.randint(1, 14)),
                date_due=today + timedelta(days=random.randint(3, 21)),
                status='active',
            )

        # Overdue loans: books[10:20] become unavailable
        for i in range(10):
            book = books[10 + i]
            book.is_available = False
            book.save()
            past_due = today - timedelta(days=random.randint(3, 30))
            Loan.objects.create(
                book=book,
                member=members[(i + 3) % len(members)],
                date_borrowed=past_due - timedelta(days=random.randint(7, 21)),
                date_due=past_due,
                status='overdue',
            )

        # Returned loans: spread across all books (books remain available)
        for i in range(10):
            borrow_date = today - timedelta(days=random.randint(30, 180))
            due_date = borrow_date + timedelta(days=14)
            return_date = borrow_date + timedelta(days=random.randint(1, 20))
            Loan.objects.create(
                book=books[i % len(books)],
                member=members[(i + 5) % len(members)],
                date_borrowed=borrow_date,
                date_due=due_date,
                date_returned=return_date,
                status='returned',
            )

        # ── Summary ────────────────────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS(
            f'\nSeeding complete:\n'
            f'  Authors  : {Author.objects.count()}\n'
            f'  Books    : {Book.objects.count()}\n'
            f'  Members  : {Member.objects.count()}\n'
            f'  Users    : {User.objects.filter(is_superuser=False).count()}\n'
            f'  Loans    : {Loan.objects.count()}\n'
            f'    Active  : {Loan.objects.filter(status="active").count()}\n'
            f'    Overdue : {Loan.objects.filter(status="overdue").count()}\n'
            f'    Returned: {Loan.objects.filter(status="returned").count()}\n'
        ))
