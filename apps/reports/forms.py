from django import forms
from .models import Report, Region


class ReportForm(forms.ModelForm):
    """Form for creating new reports"""
    
    class Meta:
        model = Report
        fields = ['victim_name', 'location', 'region', 'urgency_level', 'incident_date', 'incident_description']
        widgets = {
            'victim_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional - leave blank for anonymous reporting'
            }),
            'location': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the location of the incident'
            }),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'urgency_level': forms.Select(attrs={'class': 'form-control'}),
            'incident_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'incident_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Provide detailed information about the incident (this will be encrypted)'
            }),
        }
        help_texts = {
            'victim_name': 'You can remain anonymous by leaving this blank',
            'incident_description': 'Your information is encrypted and kept confidential',
        }


class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['status', 'assigned_to', 'urgency_level']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'urgency_level': forms.Select(attrs={'class': 'form-control'}),
        }



