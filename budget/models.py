import decimal

from django.db import models
from django.db.models import Count, Sum
import uuid

from django.urls import reverse

FREQUENCY_CHOICES = (
    ("Monthly", "Monthly"),
    ("Bimonthly", "Bimonthly"),
    ("Quarterly", "Quarterly"),
    ("Biannually", "Biannually"),
    ("Annually", "Annually"),
)

frequency_factor = {
    "Monthly": 1,
    "Bimonthly": 1 / 2,
    "Quarterly": 1 / 3,
    "Biannually": 1 / 6,
    "Annually": 1 / 12,
}


class Income(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="Monthly")
    concept = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.monthly_amount = self.amount * decimal.Decimal(frequency_factor[self.frequency])
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"INCOME: {self.concept} - {self.frequency} => {self.amount}"

    def get_absolute_url(self):
        return reverse('budget:income_detail', args=[str(self.id)])


class ItemCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    def get_num_of_spent(self):
        return Item.objects.filter(category=self).aggregate(num_of_spents=Count('id'))

    def get_total_spent(self):
        return Item.objects.filter(category=self).aggregate(total_amount=Sum('amount'))


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="Monthly")
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="categories")
    concept = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, blank=True)
    is_essential = models.BooleanField()
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.monthly_amount = self.amount * decimal.Decimal(frequency_factor[self.frequency])
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Item: {self.concept} - {self.frequency} => {self.monthly_amount}"

    def get_absolute_url(self):
        return reverse('budget:item_detail', args=[str(self.id)])
