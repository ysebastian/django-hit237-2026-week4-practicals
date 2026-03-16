# Exercise 1.2.1 – Django QuerySet: Chain Filters on the Book Model

## Python Code

```python
from catalogue.models import Book

qs = Book.objects.filter(publication_year__gt=1900, genre='Science Fiction').order_by('title')

# Print the generated SQL without evaluating the QuerySet
print(str(qs.query))

# Evaluate the QuerySet and print book titles
books = list(qs)
for book in books:
    print(book.title)
```

## Generated SQL

```sql
SELECT "catalogue_book"."id", "catalogue_book"."title", "catalogue_book"."isbn",
       "catalogue_book"."genre", "catalogue_book"."publication_year",
       "catalogue_book"."page_count", "catalogue_book"."author_id",
       "catalogue_book"."is_available"
FROM "catalogue_book"
WHERE ("catalogue_book"."genre" = 'Science Fiction'
  AND "catalogue_book"."publication_year" > 1900)
ORDER BY "catalogue_book"."title" ASC
```

## Query Count Check

```python
import django.db

django.db.reset_queries()
qs = Book.objects.filter(publication_year__gt=1900, genre='Science Fiction').order_by('title')
books = list(qs)
print(len(django.db.connection.queries))  # Output: 1
```

**Output:** `1`

Chaining `.filter()` and `.order_by()` builds a single internal query description. Django only sends one SQL statement to the database when the QuerySet is evaluated — in this case when `list()` is called. All chained operations are combined into a single `SELECT` statement, so no matter how many methods are chained, evaluation always costs exactly one database round-trip.

## Results

Books matching `publication_year > 1900` AND `genre = "Science Fiction"`, ordered by title:

| # | Title |
|---|-------|
| 1 | Dune |
| 2 | Dune Messiah |
| 3 | Foundation |
| 4 | Foundation and Empire |
| 5 | I, Robot |
| 6 | The Dispossessed |
| 7 | The Left Hand of Darkness |

**Total: 7 books**
