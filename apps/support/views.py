from django.shortcuts import render
from .models import SupportContact

# Create your views here.
def support_contact(request):
    supportcontact = SupportContact.objects.filter(is_verified=True)
    return render(request, 'support/support_contact.html', {"supportcontact":supportcontact})