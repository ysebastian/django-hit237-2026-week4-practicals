# Exercise 1.3.2 — Resolve N+1 with `select_related`

## Python Code

```python
import django.db
from catalogue.models import Loan

django.db.reset_queries()

qs = Loan.objects.select_related('book', 'member__user').all()

# Print the generated SQL without evaluating the QuerySet
print(str(qs.query))

# Evaluate and print loan details
for loan in qs:
    print(f'{loan.book.title} | {loan.member.user.username}')

print(f'Total queries: {len(django.db.connection.queries)}')
```

## Generated SQL

```sql
SELECT "catalogue_loan"."id", "catalogue_loan"."book_id",
       "catalogue_loan"."member_id", "catalogue_loan"."date_borrowed",
       "catalogue_loan"."date_due", "catalogue_loan"."date_returned",
       "catalogue_loan"."status",
       "catalogue_book"."id", "catalogue_book"."title", "catalogue_book"."isbn",
       "catalogue_book"."genre", "catalogue_book"."publication_year",
       "catalogue_book"."page_count", "catalogue_book"."author_id",
       "catalogue_book"."is_available",
       "catalogue_member"."id", "catalogue_member"."user_id",
       "catalogue_member"."library_card_number", "catalogue_member"."membership_type",
       "catalogue_member"."join_date",
       "auth_user"."id", "auth_user"."password", "auth_user"."last_login",
       "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name",
       "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff",
       "auth_user"."is_active", "auth_user"."date_joined"
FROM "catalogue_loan"
INNER JOIN "catalogue_book"
    ON ("catalogue_loan"."book_id" = "catalogue_book"."id")
INNER JOIN "catalogue_member"
    ON ("catalogue_loan"."member_id" = "catalogue_member"."id")
INNER JOIN "auth_user"
    ON ("catalogue_member"."user_id" = "auth_user"."id")
ORDER BY "catalogue_loan"."date_borrowed" DESC
```

### JOIN Clauses Identified

| JOIN | Relationship |
|------|-------------|
| `INNER JOIN "catalogue_book" ON (loan.book_id = book.id)` | `Loan → Book` (FK: `book`) |
| `INNER JOIN "catalogue_member" ON (loan.member_id = member.id)` | `Loan → Member` (FK: `member`) |
| `INNER JOIN "auth_user" ON (member.user_id = auth_user.id)` | `Member → User` (FK: `member__user`) |

## Output

```
Dune | jsmith
Dune Messiah | mjohnson
Foundation and Empire | cwilson
The Left Hand of Darkness | abrown
Foundation | rdavis
Murder on the Orient Express | kmoore
The Dispossessed | ewilliams
The ABC Murders | sthomas
I, Robot | lmiller
And Then There Were None | ptaylor
The Hobbit | sthomas
The Return of the King | abrown
Animal Farm | rdavis
The Bluest Eye | cwilson
Love in the Time of Cholera | ptaylor
One Hundred Years of Solitude | kmoore
1984 | ewilliams
Murder on the Orient Express | abrown
Beloved | lmiller
The Fellowship of the Ring | jsmith
The Two Towers | mjohnson
The Dispossessed | ptaylor
Dune Messiah | cwilson
Dune | lmiller
I, Robot | jsmith
The Left Hand of Darkness | kmoore
Foundation and Empire | mjohnson
Foundation | sthomas
And Then There Were None | ewilliams
The ABC Murders | rdavis

Total queries: 1
```

## Query Count

**1 query for 30 loans** — down from 91 in Exercise 1.3.1.

## Why `select_related` Is Appropriate Here

`select_related` is appropriate whenever the relationships being traversed are **foreign key** (or one-to-one) relationships, because SQL `INNER JOIN` can fetch the parent rows in the same `SELECT` statement at no extra round-trip cost. Both `book` and `member` on `Loan` are `ForeignKey` fields, and `user` on `Member` is a `OneToOneField` — all perfectly suited to a JOIN-based fetch.

By specifying `select_related('book', 'member__user')`, Django follows the `member → user` chain using the double-underscore path and adds a third `INNER JOIN` to `auth_user`, meaning all four tables are resolved in a single query. This eliminates the N+1 problem entirely: regardless of how many loans exist, the database is always hit exactly once.
