from django.shortcuts import render, redirect
from medicine.models import *
from django.http import JsonResponse



# Create your views here.

def home(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    print(context)
    return render(request, 'index.html', context=context)

def make_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        message = request.POST.get('message')

        print(name, date, doctor, department, message)
    # return render(request, 'index.html')
    return redirect('home')

def auth(request):
    return render(request, 'login_register.html')

def login(request):
    return redirect('home')

def register(request):

    return redirect('home')

def get_doctors(request):
    department_id = request.GET.get('department_id')


    doctors = Doctor.objects.filter(department_id=department_id).select_related('user')

    doctor_list = [
        {
            'id': doctor.id,
            'name': f'{doctor.user.first_name} {doctor.user.last_name}'
        } for doctor in doctors
    ]
    return JsonResponse(doctor_list, safe=False)





