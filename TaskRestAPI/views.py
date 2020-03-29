from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from TaskRestAPI.models import Narudzbine
# Create your views here.

def index(request):
    return render(request,'public/index.html')

