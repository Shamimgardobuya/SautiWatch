from django import forms
from .models import Report, Region


class ReportForm(forms.ModelForm):
    
    class Meta:
        model = Report
        fields = ['victim_name', 'is_anonymous', 'assaulter_name', 'assaulter_description', 'location', 'region', 'incident_date', 'description',  ]
        widgets = {
            'victim_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional - Leave blank for anonymous report'
            }),
                        'assaulter_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of the person (if known)'
            }),
            'assaulter_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Physical description, clothing, or any identifying details...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where did this incident occur?',
                'required': True
            }),
            'incident_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Please describe the incident in detail...',
                'required': True
            }),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
            
        help_texts = {
            'victim_name': 'You can remain anonymous by leaving this blank',
            'description': 'Your information is encrypted and kept confidential',
        }
    def clean(self):
        cleaned_data = super().clean()
        is_anonymous = cleaned_data.get('is_anonymous')
        victim_name = cleaned_data.get('victim_name')
        
        # If not anonymous, victim name is required
        if not is_anonymous and not victim_name:
            raise forms.ValidationError(
                "Please provide a name or select anonymous reporting."
            )
        
        return cleaned_data
class ReportSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by tracking ID, location, or description...'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + list(Report.STATUS_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    urgency = forms.ChoiceField(
        required=False,
        choices=[('', 'All Urgency Levels')] + list(Report.URGENCY_CHOICES),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    region = forms.ModelChoiceField(
        required=False,
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='All Regions'
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Region
        self.fields['region'].queryset = Region.objects.all()

    






