from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.messages import constants
from .models import DataPatient, Option, Patient, Snack
from django.views.decorators.csrf import csrf_exempt


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
            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso')
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
    patients = get_object_or_404(Patient, id=id)
    if not patients.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient-data/')        
    if request.method == "GET":
        data_patient = DataPatient.objects.filter(patient=patients)
        return render(request, 'patient_data.html', {'patient': patients, 'data_patient': data_patient})
    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')

        patients = DataPatient(patient=patients,
                        data=datetime.now(),
                        peso=peso,
                        altura=altura,
                        percentual_gordura=gordura,
                        percentual_musculo=musculo,
                        colesterol_hdl=hdl,
                        colesterol_ldl=ldl,
                        colesterol_total=colesterol_total,
                        trigliceridios=triglicerídios)

        patients.save()

        messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')

        return HttpResponseRedirect(request.path_info)


@login_required(login_url='/auth/login/')
@csrf_exempt
def chart_weight(request, id):
    patient = Patient.objects.get(id=id)
    datas = DataPatient.objects.filter(patient=patient).order_by("data")
    
    pesos = [dado.peso for dado in datas]
    labels = list(range(len(pesos)))
    data = {'peso': pesos,
            'labels': labels}
    return JsonResponse(data)


def meal_plan_list(request):
    if request.method == "GET":
        patients = Patient.objects.filter(nutri=request.user)
        return render(request, 'meal_plan_list.html', {'patients': patients})


def meal_plan(request, id):
    patients = get_object_or_404(Patient, id=id)
    if not patients.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient-data/')

    if request.method == "GET":
        snack1 = Snack.objects.filter(patient=patients).order_by('horario')
        option = Option.objects.all()
        return render(request, 'meal_plan.html', {'patient': patients, 'snack': snack1, 'option': option})


def snack(request, id_patient):
    patients = get_object_or_404(Patient, id=id_patient)
    if not patients.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/data-patient/')

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        snack1 = Snack(patient=patients,
                      titulo=titulo,
                      horario=horario,
                      carboidratos=carboidratos,
                      proteinas=proteinas,
                      gorduras=gorduras)

        snack1.save()

        messages.add_message(request, constants.SUCCESS, 'Refeição cadastrada')
        return redirect(f'/meal-plan/{id_patient}')


def option(request, id_patient):
    if request.method == "POST":
        id_snack = request.POST.get('snack')
        image = request.FILES.get('image')
        description = request.POST.get("description")

        o1 = Option(snack_id=id_snack,
                   image=image,
                   description=description)

        o1.save()

        messages.add_message(request, constants.SUCCESS, 'Opção cadastrada')
        return redirect(f'/meal-plan/{id_patient}')


@login_required(login_url='/auth/login/')
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk) 
    if 'HTTP_REFERER' in request.META:
        previous_page = request.META['HTTP_REFERER']
        patient.delete()
        messages.add_message(request, constants.SUCCESS, 'Paciente deletado!')
        return redirect(previous_page)
    return redirect(f"{request.path}")




@login_required(login_url='/auth/login/')
@csrf_exempt
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        if request.POST.get('_method') == 'patch':
            name = request.POST.get('name')
            age = request.POST.get('age')
            email = request.POST.get('email')
            telephone = request.POST.get('telephone')

            try:
                # Atribui os novos valores ao paciente
                patient.name = name
                patient.age = age
                patient.email = email
                patient.telephone = telephone

                # Salva as alterações no banco de dados
                patient.save()

                messages.add_message(request, constants.SUCCESS, 'Paciente editado com sucesso!')
                return redirect('/patients/')
            except Exception as e:
                print(e)
                messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
                return redirect('/patients/')
        else:
            # Retorna um erro se o método HTTP não for suportado
            return HttpResponseBadRequest('Método HTTP não suportado')

    # Se não for uma requisição POST, renderize a página de edição
    return render(request, 'patients.html', {'patient': patient})