from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError, OperationalError
from django.db.models import QuerySet

from .models import User, Transaction


def creates_user(username: str, email: str, password: str, cpf: str, phone_number: str = '') -> User:
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            cpf=cpf,
            phone_number=phone_number
        )
        return user

    except IntegrityError:
        raise ValidationError('One of the fields already exists: username, email, cpf or phone number')
    except OperationalError:
        raise ValidationError('Database connection error. Try again.')


def create_transaction(user: User, value: str, kind: str) -> Transaction:
    """
    Business rule:
    - User must be active
    - Kind must be valid
    - Transaction must be created atomically
    """

    # Validate kind before anything else
    valid_kind = [choice[0] for choice in Transaction.Kind.choices]
    if kind not in valid_kind:
        raise ValidationError(f'Invalid kind. Valid options: {valid_kind}')

    # Step 1 - Is the user active
    if not user.is_active:
        raise ValidationError('Inactive user.')

    # Step 2 - Create the transaction with atomic
    with transaction.atomic():
        new_transaction = Transaction.objects.create(
            user=user,
            value=value,
            kind=kind,
            status=Transaction.Status.PENDENT
        )

    new_transaction = Transaction.objects.select_related('user').get(id=new_transaction.id)
    return new_transaction


def get_all_transactions(user_id: int) -> QuerySet:
    transactions = Transaction.objects.select_related('user').filter(user=user_id)
    return transactions

