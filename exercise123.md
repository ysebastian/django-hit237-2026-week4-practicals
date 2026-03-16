# Exercise 1.2.3 — Chain Filters Across Relationships

## Python Code

```python
from catalogue.models import Author

qs = (
    Author.objects
    .filter(books__page_count__gt=300)
    .exclude(nationality='Unknown')
    .order_by('name')
    .distinct()
)

# Print the generated SQL without evaluating the QuerySet
print(str(qs.query))

# Evaluate the QuerySet and print author names
authors = list(qs)
for author in authors:
    print(author.name)
```

## Generated SQL

```sql
SELECT DISTINCT "catalogue_author"."id", "catalogue_author"."name",
       "catalogue_author"."date_of_birth", "catalogue_author"."biography",
       "catalogue_author"."nationality"
FROM "catalogue_author"
INNER JOIN "catalogue_book"
    ON ("catalogue_author"."id" = "catalogue_book"."author_id")
WHERE ("catalogue_book"."page_count" > 300
  AND NOT ("catalogue_author"."nationality" = 'Unknown'))
ORDER BY "catalogue_author"."name" ASC
```

## Query Count Check

```python
import django.db

django.db.reset_queries()
qs = (
    Author.objects
    .filter(books__page_count__gt=300)
    .exclude(nationality='Unknown')
    .order_by('name')
    .distinct()
)
authors = list(qs)
print(len(django.db.connection.queries))  # Output: 1
```

**Output:** `1`

Chaining `.filter()`, `.exclude()`, `.order_by()`, and `.distinct()` builds a single internal query description. Django only sends one SQL statement to the database when the QuerySet is evaluated — in this case when `list()` is called. All chained operations, including the cross-relationship `INNER JOIN`, are compiled into a single `SELECT DISTINCT` statement, so evaluation always costs exactly one database round-trip regardless of how many methods are chained.

## Results

Authors with at least one book of more than 300 pages, excluding authors with nationality `"Unknown"`, ordered by name:

| # | Author Name |
|---|------------|
| 1 | Frank Herbert |
| 2 | Gabriel Garcia Marquez |
| 3 | George Orwell |
| 4 | J.R.R. Tolkien |
| 5 | Toni Morrison |
| 6 | Ursula K. Le Guin |

**Total: 6 authors**
