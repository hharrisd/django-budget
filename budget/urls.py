from django.urls import path

from .views import (ItemListView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView, IncomeDetailView,
                    IncomeCreateView, IncomeUpdateView, IncomeDeleteView)

app_name = "budget"

urlpatterns = [
    # Item's paths
    path("", ItemListView.as_view(), name="item_list"),
    path("items/<uuid:pk>/detail", ItemDetailView.as_view(), name="item_detail"),
    path("items/create", ItemCreateView.as_view(), name="item_create"),
    path("items/<uuid:pk>/update", ItemUpdateView.as_view(), name="item_update"),
    path("items/<uuid:pk>/delete", ItemDeleteView.as_view(), name="item_delete"),

    # Income's paths
    path("incomes/<uuid:pk>/detail", IncomeDetailView.as_view(), name="income_detail"),
    path("incomes/create", IncomeCreateView.as_view(), name="income_create"),
    path("incomes/<uuid:pk>/update", IncomeUpdateView.as_view(), name="income_update"),
    path("incomes/<uuid:pk>/delete", IncomeDeleteView.as_view(), name="income_delete"),
]
