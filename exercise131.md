# Exercise 1.3.1 — Demonstrate the N+1 Query Problem

## Python Code

```python
import django.db
from catalogue.models import Loan

django.db.reset_queries()

loans = Loan.objects.all()
for loan in loans:
    print(f'{loan.book.title} | {loan.member.user.username}')

print(f'Total queries: {len(django.db.connection.queries)}')
print(f'Total loans: {loans.count()}')
```

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

Total queries: 91
Total loans: 30
```

## Query Count

**91 queries for 30 loans.**

## Explanation: The N+1 Problem

The query count is 91 because `Loan.objects.all()` issues **1** query to fetch all 30 loans, but then each access to `loan.book` triggers **1** additional query to fetch the related `Book`, and each access to `loan.member.user` triggers **2** more queries — one for `Member` and one for `User`. This gives roughly `1 + (30 × 3) = 91` queries in total.

The **N+1 problem** is a performance anti-pattern where fetching a list of N objects and then accessing a related object on each one results in N additional queries — one per row — instead of a single join. In this case, N is 30 loans, so Django makes 1 query to get the loans plus up to 3 queries per loan to traverse the `book` and `member → user` foreign keys, totalling 91 round-trips to the database.

The solution is to use `select_related()`, which tells Django to perform a SQL `JOIN` and fetch all related objects in a single query: `Loan.objects.select_related('book', 'member__user').all()`.
