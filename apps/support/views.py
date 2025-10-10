from django.shortcuts import render
from .models import SupportContact

# Create your views here.
def support_contact(request):
    region = request.GET.get('region','')
    category = request.GET.get('category','')
    supportcontact = SupportContact.objects.filter(is_verified=True)
    
    if region:
         supportcontact = supportcontact.filter(region__icontains=region)
    
    if category:
        supportcontact = supportcontact.filter(category=category)
    
    context ={
        "supportcontact":supportcontact,
        "region":region,
        "category":category,
        
    }
    
    return render(request, 'support/support_contact.html', context)