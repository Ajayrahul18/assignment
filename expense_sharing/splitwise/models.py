from django.db import models
# Create your models here.
from django.db import models
from .task import send_expense_email

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    mobile_number = models.CharField(max_length=20)
    expense_share_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Expense(models.Model):
    total_expense = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=200, choices=[('EQUAL', 'EQUAL'), ('EXACT', 'EXACT'), ('PERCENT', 'PERCENT')])
    users_share = models.ManyToManyField(User, related_name='expense_share')
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.expense_type == 'EQUAL':
            self.calculate_equal_amount()
        elif self.expense_type == 'EXACT':
            self.calculate_exact_amount()
        elif self.expense_type == 'PERCENT':
            self.calculate_percent_amount()

    
    def calculate_exact_amount(self):

        if self.expense_type == 'EQUAL':
            amount_per_user = self.total_expense / self.users_share.count()
            individual_expenses = []

            for user in self.users_share.all():
                user.expense_share_amount += amount_per_user
                user.save()

                individual_expenses = IndividualExpense(
                    debtor=user,
                    creditors=self.paid_by,
                    amount=amount_per_user,
                    expense=self
                )
                individual_expenses.save()
                individual_expenses.append(individual_expenses)
                send_expense_email.delay(user.email, user.exact_share)
            return individual_expenses

        elif self.expense_type == 'EXACT':
            total_exact_amount = sum(user.exact_share for user in self.users_share.all())
            if total_exact_amount != self.total_expense:
                raise ValueError("The sum of exact shares is not equal to the total amount.")

            individual_expenses = []
            for user in self.users_share.all():
                user.expense_share_amount += user.exact_share
                user.save()

                individual_expense = IndividualExpense(
                    debtor=user,
                    creditor=self.paid_by,
                    amount=user.exact_share,
                    expense=self
                )
                individual_expense.save()
                individual_expenses.append(individual_expense)
                send_expense_email.delay(user.email, user.exact_share)
                
            return individual_expenses
        elif self.expense_type == 'PERCENT':
            total_percentage_share = sum(user.percentage_share for user in self.users_share.all())
            if total_percentage_share != 100:
                raise ValueError("The sum of percentage shares is not equal to 100%.")

            individual_expenses = []
            for user in self.users_share.all():
                percentage_share = user.percentage_share
                individual_amount = (self.total_expense * percentage_share) / 100

                user.expense_share_amount += individual_amount
                user.save()

                individual_expense = IndividualExpense(
                    debtor=user,
                    creditor=self.paid_by,
                    amount=individual_amount,
                    expense=self
                )
                individual_expense.save()
                individual_expenses.append(individual_expense)
                send_expense_email.delay(user.email, user.exact_share)
            return individual_expenses
        else:
            raise ValueError("Check the amount value")




class IndividualExpense(models.Model):
    debtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debts')
    creditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)


