from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, F, Func, ExpressionWrapper, DecimalField, Case, When
from .models import Item, Income


class ItemBaseView(View):
    """Class to define the common elements for the Item's views"""
    model = Item
    fields = "__all__"
    success_url = reverse_lazy("budget:item_list")


class ItemListView(ItemBaseView, ListView):
    """View to list all the items in a budget"""
    context_object_name = "item_list"
    template_name = "budget/item_list.html"

    def get_queryset(self):
        queryset = (
            Item.objects.annotate(
                # Annotated fields to add biannually and annually amounts
                biannually_amount=F("monthly_amount") * 6,
                annually_amount=F("monthly_amount") * 12,
            )
            .select_related("category")
            .order_by('category__name', 'updated_at'))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        queryset = kwargs['object_list']

        # Calculate totals
        total_monthly_amount = 0
        total_amount_by_type = {"essential": 0, "no_essential": 0}
        category_totals = {}
        for item in queryset:
            if item.is_essential:
                total_amount_by_type["essential"] += item.monthly_amount
            else:
                total_amount_by_type["no_essential"] += item.monthly_amount

            total_monthly_amount += item.monthly_amount

            # Calculate the total amount by category
            if item.category.name in category_totals:
                category_totals[item.category.name] += item.monthly_amount
            else:
                category_totals[item.category.name] = item.monthly_amount

        # Convert the category totals into a list of dictionaries
        total_amount_by_category = [
            {'category': category, 'total_amount': total}
            for category, total in category_totals.items()
        ]

        income_list = Income.objects.annotate(
            # Annotated fields to add biannually and annually amounts
            biannually_amount=F("monthly_amount") * 6,
            annually_amount=F("monthly_amount") * 12,)

        income_totals = Income.objects.aggregate(monthly=Sum("monthly_amount"))

        kwargs.update(
            {
                "total_amount_by_category": total_amount_by_category,
                "total_amount_by_type": total_amount_by_type,
                "total_monthly_amount": total_monthly_amount,
                "income_list": income_list,
                "income_totals": income_totals,
                "monthly_cash_flow": income_totals["monthly"] - total_monthly_amount
            }
        )

        return kwargs


class ItemDetailView(ItemBaseView, DetailView):
    """View to display an item's detail"""
    context_object_name = 'item'
    template_name = "budget/item_detail.html"
    queryset = Item.objects.select_related("category")


class ItemCreateView(ItemBaseView, CreateView):
    """View to create a new item"""


class ItemUpdateView(ItemBaseView, UpdateView):
    """View to update a given item"""


class ItemDeleteView(ItemBaseView, DeleteView):
    """View to delete a given item"""


class IncomeBaseView(View):
    """Class to define the common elements for the Income's views"""
    model = Income
    fields = "__all__"
    success_url = reverse_lazy("budget:item_list")


class IncomeListView(IncomeBaseView, ListView):
    """View to list all the income in a budget"""
    context_object_name = "income_list"
    template_name = "budget/item_list.html"


class IncomeDetailView(IncomeBaseView, DetailView):
    """View to display an income's detail"""
    context_object_name = 'income'
    template_name = "budget/income_detail.html"


class IncomeCreateView(IncomeBaseView, CreateView):
    """View to create a new income"""


class IncomeUpdateView(IncomeBaseView, UpdateView):
    """View to update a given income"""


class IncomeDeleteView(ItemBaseView, DeleteView):
    """View to delete a given income"""
