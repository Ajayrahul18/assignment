
from celery import shared_task
from django.core.mail import send_mail
from schedule import every, run_every
from datetime import datetime, timedelta
from .models import User,IndividualExpense
from django.db.models import Sum
from .models import IndividualExpense

@shared_task
def send_expense_email(user_email, expense_amount):
    subject = 'New Expense Added'
    message = f'You have been added to a new expense. You owe Rs {expense_amount}.'
    from_email = 'thiyalanaj@example.com'
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_weekly_email():
    # Get all users
    users = User.objects.all()

    for user in users:
        total_amount_owed = calculate_total_amount_owed(user)  # You need to implement this function
        send_mail(
            'Weekly Expense Summary',
            f'You owe a total of Rs {total_amount_owed} to other users.',
            'thiyalanaj@example.com',
            [user.email],
            fail_silently=False,
        )

# Schedule the task to run every week
run_every(send_weekly_email, every(1).weeks, at=datetime.now() + timedelta(seconds=10))

def calculate_total_amount_owed(user):
    debts = IndividualExpense.objects.filter(debtor=user)

    total_amount_owed = debts.aggregate(sum('amount'))['amount__sum'] or 0 

    return total_amount_owed
