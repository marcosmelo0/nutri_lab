from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.messages import constants
from .models import DataPatient, Patient


@login_required(login_url='/auth/login')
def patient(request):
    if request.method == "GET":
        patients = Patient.objects.filter(nutri=request.user)
        return render(request, 'patients.html', {'patients': patients})
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


@login_required(login_url='/auth/logar/')
def patient_data_list(request):
    if request.method == "GET":
        patients = Patient.objects.filter(nutri=request.user)
        return render(request, 'patients_data_list.html', {'patients': patients})


@login_required(login_url='/auth/login/')
def patient_data(request, id):
    patient = get_object_or_404(Patient, id=id)
    if not patient.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient-data/')
        
    if request.method == "GET":
        data_patient = DataPatient.objects.filter(paciente=patient)
        return render(request, 'patient_data.html', {'patient': patient, 'data_patient': data_patient})
    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')

        patient = DataPatient(paciente=patient,
                        data=datetime.now(),
                        peso=peso,
                        altura=altura,
                        percentual_gordura=gordura,
                        percentual_musculo=musculo,
                        colesterol_hdl=hdl,
                        colesterol_ldl=ldl,
                        colesterol_total=colesterol_total,
                        trigliceridios=triglicerídios)

        patient.save()

        messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')

        return HttpResponseRedirect(request.path_info)
