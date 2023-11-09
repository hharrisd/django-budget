from django.contrib import admin
from .models import Income, Item, ItemCategory


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("frequency", "concept", "amount",)


class ItemInline(admin.TabularInline):
    model = Item
    list_display = ("frequency", "concept", "amount", "is_essential", "transaction_date",)


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    list_display = ("name",)
