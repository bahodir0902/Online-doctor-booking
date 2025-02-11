from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    return render(request, 'index.html')

def make_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        message = request.POST.get('message')

        print(name, email, phone, date, doctor, department, message)
    # return render(request, 'index.html')
    return redirect('home')

def auth(request):
    return render(request, 'login_register.html')

def login(request):
    return redirect('home')

def register(request):
    return redirect('home')