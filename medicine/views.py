from django.shortcuts import render, redirect
from medicine.models import *
from django.http import JsonResponse
from _datetime import datetime, timedelta


# Create your views here.

def home(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    # print(context)
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


def get_available_dates(request):
    doctor_id = request.GET.get('doctor_id')
    available_dates = Availability.objects.filter(doctor_id=doctor_id)
    working_days = []
    for date in available_dates:
        date = str(date).split()
        working_days.append(date[0])

    today = datetime.today()
    next_week = today + timedelta(days=7)
    current_date = today
    result = []
    while current_date <= next_week:
        if current_date.strftime('%A') in working_days:
            d = {}
            d['date'] = current_date.strftime('%Y-%m-%d')
            d['display'] = f'{current_date.strftime('%d-%m-%Y')}, {current_date.strftime('%A')}'
            result.append(d)
        current_date += timedelta(days=1)

    return JsonResponse(result, safe=False)


def get_available_datetime(request):
    doctor_id = request.GET.get('doctor_id')
    selected_date = request.GET.get('date')
    date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    weekday = date_obj.strftime('%A')
    print(weekday)
    # here would be mine actual logic for finding available times
    times = str(Availability.objects.filter(doctor_id=doctor_id, days_of_week=weekday)).split()
    start_time = times[3][1:]
    end_time = times[5][:-4]
    print(start_time, end_time)


    available_slots = ['09:00', '10:30', '13:00', '15:30']  # This should come from your scheduling logic
    return JsonResponse(available_slots, safe=False)


