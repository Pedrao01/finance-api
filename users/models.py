from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=13, blank=True)
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f'{self.email}'


class Transaction(models.Model):
    class Kind(models.TextChoices):
        DEBT = 'debit', 'Debit'
        CREDIT = 'credit', 'Credit'

    class Status(models.TextChoices):
        PENDENT = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='transactions'
    )

    value = models.DecimalField(max_digits=11, decimal_places=2)
    kind = models.CharField(max_length=10, choices=Kind.choices)
    status = models.CharField(max_length=10, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.kind} - R$ {self.value}'