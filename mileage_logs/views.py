from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import MonthlyMileageLog
from .forms import MileageLogEntryFormSet, MileageClaimFormSet, MonthlyMileageLogForm


class MileageLogListView(ListView):
    """
    Generic view to list all MonthlyMileageLog entries.
    """
    model = MonthlyMileageLog
    template_name = 'mileage_logs/list_mileage_logs.html'
    context_object_name = 'monthly_logs'
    queryset = MonthlyMileageLog.objects.all().order_by('-year', '-month')

class MileageLogDetailView(DetailView):
    """
    Generic view to display a single MonthlyMileageLog entry.
    """
    model = MonthlyMileageLog
    template_name = 'mileage_logs/detail_mileage_log.html'
    context_object_name = 'monthly_log'

def create_mileage_log_view(request):
    """
    View to create a new MonthlyMileageLog and its nested inlines.
    """
    monthly_log_form = MonthlyMileageLogForm(request.POST or None)
    formset = MileageLogEntryFormSet(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if monthly_log_form.is_valid() and formset.is_valid():
            monthly_log = monthly_log_form.save(commit=False)
            monthly_log.save()

            instances = formset.save(commit=False)
            for instance in instances:
                instance.monthly_log = monthly_log
                instance.save()
            formset.save_m2m()

            return redirect('list_mileage_logs')  # Redirect to the list view after creation

    context = {
        'monthly_log_form': monthly_log_form,
        'formset': formset,
    }
    return render(request, 'mileage_logs/add_mileage_log.html', context)

def update_mileage_log_view(request, pk):
    """
    View to update a MonthlyMileageLog and its nested inlines.
    """
    monthly_log = get_object_or_404(MonthlyMileageLog, pk=pk)

    if request.method == 'POST':
        formset = MileageLogEntryFormSet(request.POST, request.FILES, instance=monthly_log)
        
        # We need to process the nested formsets as well.
        # This is a bit more complex, but here's a basic structure.
        claim_formsets = []
        if formset.is_valid():
            # Save parent forms first
            instances = formset.save(commit=False)
            
            # Loop through all forms in the formset
            for form in formset.ordered_forms:
                if form.instance.pk:
                    # If it's an existing instance, process its claim formset.
                    claim_formset = MileageClaimFormSet(request.POST, request.FILES, instance=form.instance, prefix=f'claims_{form.instance.pk}')
                    if claim_formset.is_valid():
                        claim_formset.save()
                    claim_formsets.append(claim_formset)
            
            # Save parent instances
            formset.save()
            return redirect('success_page') # Replace with your success URL
    
    else: # GET request
        formset = MileageLogEntryFormSet(instance=monthly_log)
        
        # Auto-populate the start_mileage for the new form
        # This is the server-side logic you requested.
        last_entry = monthly_log.log_entries.order_by('-entry_date', '-start_mileage').first()
        if last_entry and formset.forms:
            # Find the empty form in the formset.
            # The last form is usually the empty one provided by `extra=1`.
            empty_form = formset.forms[-1]
            if not empty_form.instance.pk:
                empty_form.initial['start_mileage'] = last_entry.end_mileage
        
    context = {
        'formset': formset,
        'monthly_log': monthly_log,
    }
    
    return render(request, 'mileage_logs/update_mileage.html', context)
