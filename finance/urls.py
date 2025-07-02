
from django.urls import path
from .views import RegisterView ,Dashboard,TransactionCreateView,TransactionListView,GoalCreateView,export_transactions

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('', Dashboard.as_view(), name="dashboard"),
    path('transaction/add/', TransactionCreateView.as_view(), name="transaction_add"),
    path('transactions/', TransactionListView.as_view(), name="transaction_list"),
    path('goal/add', GoalCreateView.as_view(), name="goal_add"),
    path('generate-report/', export_transactions, name="export_transactions"),
]


