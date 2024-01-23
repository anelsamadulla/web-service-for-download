from django import forms

class DataSenderForm(forms.Form):
    company = forms.CharField(max_length=100)  # Additional info.
    fname = forms.CharField(max_length=50)  # Additional info.
    lname = forms.CharField(max_length=50)  # Additional info.
    patronym = forms.CharField(max_length=50)  # Additional info.
    
    status_choices = [
        (1, 'Pending'),
        (2, 'Completed'),
        (3, 'Failed')
    ]
    status = forms.ChoiceField(
        choices=status_choices,
        widget=forms.RadioSelect,
        required=True
    )

    amount = forms.IntegerField()  # Payment amount
    created_at = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    expires_at = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    
    issued_for = forms.CharField(max_length=100)  # License info
    device_id = forms.CharField(max_length=50)  # Unique number of the device
    devices = forms.IntegerField()
    
    services_choices = [
        (1, 'Service 1'),
        (2, 'Service 2'),
        (3, 'Service 3')
    ]
    services = forms.MultipleChoiceField(
        choices=services_choices,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean_services(self):
        services_input = self.cleaned_data['services']

        # Ensure the 'services' field is not empty
        if not services_input:
            raise forms.ValidationError("Please choose at least one service.")

        return [int(service) for service in services_input]
