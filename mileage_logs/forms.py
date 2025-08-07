from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Row, Column, HTML
from .models import MonthlyMileageLog, MileageLogEntry, MileageClaim

# --- Form for the parent MonthlyMileageLog model ---
class MonthlyMileageLogForm(forms.ModelForm):
    """
    Custom form for the MonthlyMileageLog, used for creation.
    """
    class Meta:
        model = MonthlyMileageLog
        fields = ['vehicle', 'year', 'month', 'start_odometer_reading', 'end_odometer_reading']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # The parent template will handle the form tag
        self.helper.layout = Layout(
            'vehicle',
            Row(
                Column('year', css_class='col-md-6'),
                Column('month', css_class='col-md-6'),
                css_class='g-3'
            ),
            Row(
                Column('start_odometer_reading', css_class='col-md-6'),
                Column('end_odometer_reading', css_class='col-md-6'),
                css_class='g-3'
            )
        )

# --- Form for a single MileageLogEntry ---
# This is the base form that will be used in our formset.
class MileageLogEntryForm(forms.ModelForm):
    """
    Custom form for MileageLogEntry, with a Crispy Forms layout.
    """
    class Meta:
        model = MileageLogEntry
        fields = ['entry_date', 'start_mileage', 'end_mileage', 'destination', 'purpose']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # The parent template will handle the form tag
        self.helper.layout = Layout(
            # Using a row to put the date and mileage fields side-by-side
            Row(
                Column('entry_date', css_class='col-md-3'),
                Column('start_mileage', css_class='col-md-3'),
                Column('end_mileage', css_class='col-md-3'),
                css_class='g-3'
            ),
            'description'
        )

    def clean(self):
        """
        Custom validation to ensure start_mileage is less than or equal to end_mileage.
        """
        cleaned_data = super().clean()
        start_mileage = cleaned_data.get('start_mileage')
        end_mileage = cleaned_data.get('end_mileage')
        
        if start_mileage is not None and end_mileage is not None:
            if start_mileage > end_mileage:
                self.add_error(
                    'start_mileage',
                    "Start mileage cannot be greater than end mileage."
                )
        return cleaned_data


# --- Formset for MileageClaim (nested inline) ---
# This formset will be used within each MileageLogEntryForm.
MileageClaimFormSet = inlineformset_factory(
    MileageLogEntry,
    MileageClaim,
    fields=('member', 'number_of_seats_claimed'),
    extra=1,
    can_delete=True,
    widgets={
        'member': forms.TextInput(attrs={'class': 'form-control member-autocomplete'}),
        'number_of_seats_claimed': forms.TextInput(attrs={'class': 'form-control', 'size': '5'}),
    }
)


# --- Formset for MileageLogEntry (main inline) ---
# This is the primary formset that will handle all trip entries.
# We set `can_delete` to True to allow users to remove entries.
MileageLogEntryFormSet = inlineformset_factory(
    MonthlyMileageLog,
    MileageLogEntry,
    form=MileageLogEntryForm,
    extra=1,
    can_delete=True
)
