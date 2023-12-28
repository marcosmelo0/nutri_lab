from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages import constants
from .models import Patient


@login_required(login_url='/auth/login')
def patient(request):
    if request.method == "GET":
        return render(request, 'patients.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')

        if (len(name.strip()) == 0) or (len(sex.strip()) == 0) or (len(age.strip()) == 0) or (len(email.strip()) == 0) or (len(telephone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/patients/')

        if not age.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
            return redirect('/patients/')

        patients = Patient.objects.filter(email=email)

        if patients.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
            return redirect('/patients/')
        try:
            patient = Patient(name=name, sex=sex, age=age, email=email, telephone=telephone, nutri=request.user)

            patient.save()
            messages.add_message(request, constants.SUCCESS, 'Paciênte cadastrado com sucesso')
            return redirect('/patients/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/patients/')

        return HttpResponse(f"{name}, {sex}, {age}, {email}, {telephone}")
