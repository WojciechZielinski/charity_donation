from django.contrib import admin

# Register your models here.
from charity_app.models import Donation, Category, Institution

admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution)