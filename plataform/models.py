from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    choices_sex = (('F', 'Feminino'), ('M', 'Masculino'))
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1, choices=choices_sex)
    age = models.IntegerField()
    email = models.EmailField()
    telephone = models.CharField(max_length=19)
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class DataPatient(models.Model):
    paciente = models.ForeignKey(Patient, on_delete=models.CASCADE)
    data = models.DateTimeField()
    peso = models.IntegerField()
    altura = models.IntegerField()
    percentual_gordura = models.IntegerField()
    percentual_musculo = models.IntegerField()
    colesterol_hdl = models.IntegerField()
    colesterol_ldl = models.IntegerField()
    colesterol_total = models.IntegerField()
    trigliceridios = models.IntegerField()

    def __str__(self):
        return f"Paciente({self.paciente.name}, {self.peso})"
