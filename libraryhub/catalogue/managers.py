from django.db import models


class LoanQuerySet(models.QuerySet):
    """Custom QuerySet for Loan model with filtering methods."""

    def active(self):
        """Returns loans where status is 'active'."""
        return self.filter(status='active')

    def for_member(self, member):
        """Accepts a Member instance and returns loans for that member."""
        return self.filter(member=member)


class LoanManager(models.Manager):
    """Custom manager for Loan model."""

    def get_queryset(self):
        """Return the custom LoanQuerySet."""
        return LoanQuerySet(self.model, using=self._db)

    def active(self):
        """Returns loans where status is 'active'."""
        return self.get_queryset().active()

    def for_member(self, member):
        """Accepts a Member instance and returns loans for that member."""
        return self.get_queryset().for_member(member)
