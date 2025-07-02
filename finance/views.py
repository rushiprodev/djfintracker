from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib import messages

from finance.form import RegisterForms, TransactionForm, GoalForm
from .models import Transcation, Goal
from .admin import TransactionResource

from import_export.formats.base_formats import XLSX


# for Registration view 
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForms()
        return render(request, 'finance/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForms(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            messages.success(request, 'Account Created Successfully')
            return redirect('dashboard')  # Redirect to home or dashboard
        return render(request, 'finance/register.html', {'form': form})  # ✅ fixed template path


# Dashboard View
class Dashboard(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        transactions = Transcation.objects.filter(user=request.user)
        goals = Goal.objects.filter(user=request.user)

        total_income = transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_savings = total_income - total_expense
        remaining_savings = net_savings

        goal_progress = []
        for goal in goals:
            if remaining_savings >= goal.target_amount:
                goal_progress.append({'goal': goal, 'progress': 100})
                remaining_savings -= goal.target_amount
            elif remaining_savings > 0:
                progress = (remaining_savings / goal.target_amount) * 100
                goal_progress.append({'goal': goal, 'progress': progress})
                remaining_savings = 0
            else:
                goal_progress.append({'goal': goal, 'progress': 0})

        context = {
            'transactions': transactions,
            'goals': goals,
            'total_income': total_income,
            'total_expense': total_expense,
            'net_savings': net_savings,
            'goal_progress': goal_progress,
        }
        return render(request, 'finance/dashboard.html', context)


# Transaction Create View
class TransactionCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        return render(request, 'finance/transcation_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction Added Successfully')
            return redirect('dashboard')
        return render(request, 'finance/transcation_form.html', {'form': form})


# Transaction List View
class TransactionListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        transactions = Transcation.objects.filter(user=request.user)
        return render(request, 'finance/transcation_list.html', {'transactions': transactions})


# Goal Create View
class GoalCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = GoalForm()
        return render(request, 'finance/goal_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Goal Created Successfully')
            return redirect('dashboard')
        return render(request, 'finance/goal_form.html', {'form': form})


# Export Transactions to Excel
def export_transactions(request):
    # Get transactions only for the logged-in user
    user_transactions = Transcation.objects.filter(user=request.user)

    # Use the resource to export the queryset
    transaction_resource = TransactionResource()
    dataset = transaction_resource.export(user_transactions)

    # Use XLSX format to export data
    export_format = XLSX()
    exported_data = export_format.export_data(dataset)

    # Create HTTP response with Excel MIME type
    response = HttpResponse(
        exported_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Set download headers
    response['Content-Disposition'] = 'attachment; filename="transactions_report.xlsx"'

    return response







# this is for practice 
# # function Based Views 

# from django.http import HttpResponse


# def home(request):
#     return HttpResponse("Welcome to the Home Page!")


# #class based views 

# # class HomeView(View):
# #     def get(self, request, *args, **kwargs):
# #         return HttpResponse("Hello Django")

# class HomeView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request,"finance/home.html")

