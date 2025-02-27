from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import UserLoginForm, UserRegisterModelForm, ForgotPasswordForm, PassCodeVerification
from .service import send_email_verification, send_password_verification
from .models import CodeEmail, CodePassword
from django.utils import timezone
from .utils import generate_unique_username
from django_ratelimit.decorators import ratelimit


# Create your views here.
def auth(request):
    login_form = UserLoginForm()
    register_form = UserRegisterModelForm()
    context = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'login_register.html', context=context)


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user_db = get_user_model().objects.filter(email=email).first()
            if not user_db:
                form.add_error(None, 'password or username is incorrect.')
                return render(request, 'login_register.html', {'login_form': form, 'register_form': UserRegisterModelForm()})

            user = authenticate(request, username=user_db.username, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'password or username is incorrect.')

            return render(request, 'login_register.html', {'login_form': form, 'register_form': UserRegisterModelForm()})


    login_form = UserLoginForm()
    register_form = UserRegisterModelForm()
    data = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'login_register.html', data)


def register(request):
    if request.method == 'POST':
        form = UserRegisterModelForm(request.POST)
        if form.is_valid():
            request.session['new_user'] = form.cleaned_data
            print(form.cleaned_data)
            return redirect('accounts:verify_email')
        form.add_error(None, "Registration failed. Please check the details.")
        return redirect('accounts:register')

    login_form = UserLoginForm()
    register_form = UserRegisterModelForm()
    data = {
        'login_form': login_form,
        'register_form': register_form
    }
    return render(request, 'login_register.html', data)


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


def verify_email(request):
    user_data = request.session.get('new_user')
    first_name = user_data.get('first_name')
    email = user_data.get('email')
    if request.method == 'POST':
        print(user_data)
        passcode = request.POST.get('activation_code')

        if not passcode:
            return HttpResponse('Some error occurred.')

        code = CodeEmail.objects.filter(email=email).first()
        if not code:
            return HttpResponse('Some error occurred')

        if code.expire_date < timezone.now():
            return HttpResponse('Code is already expired')

        if code.code_number != passcode:
            return redirect('accounts:verify_email')

        form = UserRegisterModelForm(user_data)
        user = form.save(commit=False)
        user.username = generate_unique_username()
        try:
            del request.session['new_user']
        except Exception as e:
            print(e)

        user.set_password(form.cleaned_data.get('password'))
        user.save()
        login(request, user)
        return redirect('home')


    send_email_verification(email, first_name)
    return render(request, 'verify_email.html')


@ratelimit(key='ip', rate='5/m', block=True)
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        print(form)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            user_db = get_user_model().objects.filter(email=email).first()
            print(user_db)
            if not user_db:
                form.add_error('email', 'email doesn\'t exists.')
                return render(request, 'reset_password.html', {'form': form})
            print(user_db.first_name)
            send_password_verification(user_db)
            request.session['email'] = email

            return render(request, 'check_email.html')

    form = ForgotPasswordForm()
    return render(request, 'reset_password.html', {'form': form})

@ratelimit(key='ip', rate='6/m', block=True)
def verify_code(request):
    form = PassCodeVerification()
    if request.method == 'POST':
        passcode = request.POST.get('verification_code')
        email = request.session.get('email')
        user_db = get_user_model().objects.filter(email=email).first()
        if not user_db:
            form.add_error('code', 'User doesn\'t exists')
            return render(request, 'check_email.html', {'forms': form})

        code_db = CodePassword.objects.filter(user_id=user_db.id).first()
        if not code_db:
            form.add_error('code', 'Code doesn\'t exists')
            return render(request, 'check_email.html', {'forms': form})

        if code_db.expire_date < timezone.now():
            form.add_error('code', 'Code is expired')
            return render(request, 'check_email.html', {'forms': form})

        if code_db.code_number != passcode:
            form.add_error('code', 'Code doesn\'t match')
            return render(request, 'check_email.html', {'forms': form})

        request.session['email'] = email
        code_db.delete()
        return render(request, 'create_new_password.html')


    return render(request, 'check_email.html')

@ratelimit(key='ip', rate='5/m', block=True)
def create_new_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return HttpResponse('Passwords doesn\'t match')

        email = request.session.get('email')
        user_db = get_user_model().objects.filter(email=email).first()

        if not user_db:
            return HttpResponse('User doesn\'t exists.')

        user_db.set_password(password)
        user_db.save()
        try:
            del request.session['email']
        except Exception as e:
            print(e)

        return redirect('accounts:login')

    return render(request, 'create_new_password.html')


def profile(request):
    return render(request, 'profile.html')