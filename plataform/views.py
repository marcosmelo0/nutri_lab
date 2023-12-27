from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/auth/login')
def patients(request):
    return render(request, 'patients.html')