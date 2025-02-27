from django.shortcuts import render, redirect, HttpResponse
from medicine.models import *
from django.http import JsonResponse
from _datetime import datetime, timedelta
from django.contrib.auth import logout, authenticate, login as login_user
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm


# Create your views here.

def home(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    # print(context)
    return render(request, 'index.html', context=context)


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

    times = str(Availability.objects.filter(doctor_id=doctor_id, days_of_week=weekday)).split()
    if len(times) < 6:
        return JsonResponse([], safe=False)

    start_time = datetime.strptime(times[3][1:], '%H:%M:%S').time()
    end_time = datetime.strptime(times[5][:-4], '%H:%M:%S').time()
    actual_end_time = datetime.combine(date_obj, end_time)
    now = datetime.now()
    step = timedelta(minutes=30)
    current_time = max(datetime.combine(date_obj, start_time), now)

    booked_slots = Appointment.objects.filter(doctor_id=doctor_id, status__in=('Pending', 'Confirmed') , datetime__date=date_obj.date())
    booked_times = {appt.datetime.strftime('%H:%M:%S') for appt in booked_slots}

    available_slots = []
    while current_time.time() <= actual_end_time.time():
        temp = current_time.strftime('%H:%M:%S')
        if temp not in booked_times:
            available_slots.append(temp)
        current_time += step

    return JsonResponse(available_slots, safe=False)


@login_required(login_url='/auth', redirect_field_name=None)
def make_appointment(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message')

        print(department, doctor, date, time, message)
    # return render(request, 'index.html')
    return redirect('home')


