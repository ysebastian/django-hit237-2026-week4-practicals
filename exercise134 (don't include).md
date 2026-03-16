# Exercise 1.3.4 — Use prefecth objects with filtering

## Python Code

```python
import django.db
from django.db.models import Prefetch
from catalogue.models import Member, Loan

django.db.reset_queries()

members = Member.objects.select_related('user').prefetch_related(
    Prefetch(
        'loans',
        queryset=Loan.objects.filter(status='active').select_related('book'),
        to_attr='active_loans'
    )
)

for member in members:
    print(f'{member.user.username} | active loans: {len(member.active_loans)}')
    for loan in member.active_loans:
        print(f'  - {loan.book.title}')

print(f'Total queries: {len(django.db.connection.queries)}')
```

## Generated SQL

Two queries are issued when the QuerySet is evaluated:

**Query 1 — Fetch all members with their user (JOIN):**

```sql
SELECT "catalogue_member"."id", "catalogue_member"."user_id",
       "catalogue_member"."library_card_number", "catalogue_member"."membership_type",
       "catalogue_member"."join_date",
       "auth_user"."id", "auth_user"."password", "auth_user"."last_login",
       "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name",
       "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff",
       "auth_user"."is_active", "auth_user"."date_joined"
FROM "catalogue_member"
INNER JOIN "auth_user"
    ON ("catalogue_member"."user_id" = "auth_user"."id")
ORDER BY "auth_user"."username" ASC
```

**Query 2 — Fetch all active loans with their book for the collected member IDs:**

```sql
SELECT "catalogue_loan"."id", "catalogue_loan"."book_id",
       "catalogue_loan"."member_id", "catalogue_loan"."date_borrowed",
       "catalogue_loan"."date_due", "catalogue_loan"."date_returned",
       "catalogue_loan"."status",
       "catalogue_book"."id", "catalogue_book"."title", "catalogue_book"."isbn",
       "catalogue_book"."genre", "catalogue_book"."publication_year",
       "catalogue_book"."page_count", "catalogue_book"."author_id",
       "catalogue_book"."is_available"
FROM "catalogue_loan"
INNER JOIN "catalogue_book"
    ON ("catalogue_loan"."book_id" = "catalogue_book"."id")
WHERE ("catalogue_loan"."status" = 'active'
  AND "catalogue_loan"."member_id" IN (13, 17, 14, 11, 18, 16, 12, 19, 15, 20))
ORDER BY "catalogue_loan"."date_borrowed" DESC
```

## Output

```
abrown | active loans: 1
  - The Left Hand of Darkness
cwilson | active loans: 1
  - Foundation and Empire
ewilliams | active loans: 1
  - The Dispossessed
jsmith | active loans: 1
  - Dune
kmoore | active loans: 1
  - Murder on the Orient Express
lmiller | active loans: 1
  - I, Robot
mjohnson | active loans: 1
  - Dune Messiah
ptaylor | active loans: 1
  - And Then There Were None
rdavis | active loans: 1
  - Foundation
sthomas | active loans: 1
  - The ABC Murders

Total queries: 2
```

## Query Count

**2 queries for 10 members** — confirmed.

## The Purpose of `to_attr`

The `to_attr` parameter stores the prefetched results as a plain Python **list** on each model instance under a custom attribute name (`active_loans`), instead of replacing the default related manager (`member.loans`). This is essential when using a **filtered prefetch** — without `to_attr`, Django would overwrite the `loans` manager with only the filtered subset, causing confusion if `member.loans.all()` is called elsewhere and unexpectedly returns only active loans. By storing the filtered results under a distinct name (`member.active_loans`), the default `member.loans` manager remains unaffected and continues to return all loans via a fresh database query, while `member.active_loans` gives fast, cache-based access to only the pre-filtered subset.
