# Exercise 1.3.3 — Use `prefetch_related` for reverse relationships

## Python Code

```python
import django.db
from catalogue.models import Author

django.db.reset_queries()

qs = Author.objects.prefetch_related('books')

for author in qs:
    print(f'{author.name} | books: {author.books.count()}')

print(f'Total queries: {len(django.db.connection.queries)}')
```

## Generated SQL

Two queries are issued when the QuerySet is evaluated:

**Query 1 — Fetch all authors:**

```sql
SELECT "catalogue_author"."id", "catalogue_author"."name",
       "catalogue_author"."date_of_birth", "catalogue_author"."biography",
       "catalogue_author"."nationality"
FROM "catalogue_author"
ORDER BY "catalogue_author"."name" ASC
```

**Query 2 — Fetch all related books in one batch:**

```sql
SELECT "catalogue_book"."id", "catalogue_book"."title", "catalogue_book"."isbn",
       "catalogue_book"."genre", "catalogue_book"."publication_year",
       "catalogue_book"."page_count", "catalogue_book"."author_id",
       "catalogue_book"."is_available"
FROM "catalogue_book"
WHERE "catalogue_book"."author_id" IN (11, 9, 14, 12, 15, 16, 13, 10)
ORDER BY "catalogue_book"."title" ASC
```

## Output

```
Agatha Christie | books: 3
Frank Herbert | books: 2
Gabriel Garcia Marquez | books: 2
George Orwell | books: 3
Isaac Asimov | books: 3
J.R.R. Tolkien | books: 4
Toni Morrison | books: 2
Ursula K. Le Guin | books: 2

Total queries: 2
```

## Query Count

**2 queries for 8 authors** — exactly as expected.

## Why `prefetch_related` Uses Two Queries Instead of a JOIN

`prefetch_related` issues two separate `SELECT` statements rather than a single `JOIN` because it is designed for **reverse foreign key and many-to-many** relationships, where a JOIN would produce duplicate parent rows (one per related child). Instead, Django fetches all parent objects in the first query, collects their IDs, and issues a second `SELECT ... WHERE author_id IN (...)` to fetch all related books at once — then stitches the results together in Python.

This strategy is preferable to `select_related` when the relationship is one-to-many (one author → many books), because a `JOIN` approach would return one row per book, causing the author data to be repeated for every book they wrote. `prefetch_related` avoids this redundancy and is also well-suited to many-to-many relationships, which cannot be expressed as a simple `INNER JOIN` without duplication. Use `select_related` for `ForeignKey`/`OneToOneField` traversals (many-to-one), and `prefetch_related` for reverse FK and many-to-many traversals (one-to-many, many-to-many).
