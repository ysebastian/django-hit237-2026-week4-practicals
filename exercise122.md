# Exercise 1.2.2 — Django QuerySet: Chain Filters on the Loan Model

## Python Code

```python
from catalogue.models import Loan

qs = Loan.objects.filter(status='overdue').order_by('date_due')

# Print the generated SQL without evaluating the QuerySet
print(str(qs.query))

# Evaluate the QuerySet and print loan details
loans = list(qs)
for loan in loans:
    print(f'{loan.book.title} | Due: {loan.date_due}')
```

## Generated SQL

```sql
SELECT "catalogue_loan"."id", "catalogue_loan"."book_id",
       "catalogue_loan"."member_id", "catalogue_loan"."date_borrowed",
       "catalogue_loan"."date_due", "catalogue_loan"."date_returned",
       "catalogue_loan"."status"
FROM "catalogue_loan"
WHERE "catalogue_loan"."status" = 'overdue'
ORDER BY "catalogue_loan"."date_due" ASC
```

## Query Count Check

```python
import django.db

django.db.reset_queries()
qs = Loan.objects.filter(status='overdue').order_by('date_due')
loans = list(qs)
print(len(django.db.connection.queries))  # Output: 1
```

**Output:** `1`

Chaining `.filter()` and `.order_by()` builds a single internal query description. Django only sends one SQL statement to the database when the QuerySet is evaluated — in this case when `list()` is called. All chained operations are combined into a single `SELECT` statement, so no matter how many methods are chained, evaluation always costs exactly one database round-trip.

## Results

Loans matching `status = "overdue"`, ordered by due date ascending (as of 2026-03-14):

| # | Book Title | Date Due |
|---|-----------|----------|
| 1 | Beloved | 2026-02-12 |
| 2 | The Two Towers | 2026-02-13 |
| 3 | The Fellowship of the Ring | 2026-02-15 |
| 4 | One Hundred Years of Solitude | 2026-02-17 |
| 5 | The Bluest Eye | 2026-02-22 |
| 6 | 1984 | 2026-02-23 |
| 7 | Love in the Time of Cholera | 2026-02-26 |
| 8 | Animal Farm | 2026-03-01 |
| 9 | The Return of the King | 2026-03-05 |
| 10 | The Hobbit | 2026-03-06 |

**Total: 10 loans**
