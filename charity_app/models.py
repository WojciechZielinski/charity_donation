from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    CHOICES = (
        (0, 'fundacja'),
        (1, 'organizacja pozarządowa'),
        (2, 'zbiórka lokalna')
    )
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.IntegerField(choices=CHOICES, default=0)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.CharField(max_length=64)
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=9)
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True)
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
