from django.contrib import admin
from .models import *
from .views import *
# Register your models here.
# admin.py

admin.site.register(User)
admin.site.register(Expense)
admin.site.register(IndividualExpense)