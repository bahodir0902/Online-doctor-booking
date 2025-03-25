from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, redirect
from medicine.models import Appointment, Notification
from .forms import UserLoginForm, UserRegisterModelForm, ForgotPasswordForm, PassCodeVerification, UserProfileModelForm
from .service import send_email_verification, send_password_verification, send_email_to_verify_email
from .models import CodeEmail, CodePassword, Doctor, CustomUser
from django.utils import timezone
from .utils import generate_unique_username, login_required, has_permission
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group


# Create your views here.
def auth(request):
    user_agent = request.META.get('HTTP_USER_AGENT', 'No agent')
    print(user_agent)
    
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
                return render(request, 'login_register.html',
                              {'login_form': form, 'register_form': UserRegisterModelForm()})

            user = authenticate(request, username=user_db.username, password=password)

            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'password or username is incorrect.')

            return render(request, 'login_register.html',
                          {'login_form': form, 'register_form': UserRegisterModelForm()})

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
        users_group, _ = Group.objects.get_or_create(name='Users')
        user.groups.add(users_group)
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


@login_required
@permission_required('accounts.can_access_doctor_dashboard', raise_exception=True)
def doctor_dashboard(request):
    doctor = Doctor.objects.filter(user_id=request.user.pk).first()
    upcoming_appointments = Appointment.objects.filter(Q(doctor=doctor) & Q(status=Appointment.Status.PENDING)).count()
    unread_notifications = Notification.objects.filter(Q(user_id=request.user.pk) & Q(is_read=False)).count()
    total_patients = Appointment.objects.filter(
        Q(doctor=doctor) & Q(status=Appointment.Status.COMPLETED)).distinct().count()

    patients = Appointment.objects.filter(Q(doctor=doctor) & Q(status=Appointment.Status.PENDING)).order_by('datetime')

    data = {
        'upcoming_appointments': upcoming_appointments,
        'unread_notifications': unread_notifications,
        'total_patients': total_patients,
        'patients': patients
    }
    return render(request, 'doctor_home_page.html', context=data)


@login_required
def profile(request):
    doctor = Doctor.objects.filter(user_id=request.user.pk).first()
    form = UserProfileModelForm(instance=request.user)

    data = {
        'bio': doctor.biography,
        'form': form
    }
    return render(request, 'profile.html', context=data)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileModelForm(request.POST, instance=user)
        if form.is_valid():
            new_email = form.cleaned_data.get('email')
            new_username = form.cleaned_data.get('username')

            if new_email != user.email and CustomUser.objects.filter(email=new_email).exists():
                form.add_error('username', 'Email already exists. Please try another one')
                return render(request, 'profile_edit.html', {'form': form})
            if new_username != user.username and CustomUser.objects.filter(username=new_username).exists():
                form.add_error('username', 'Username already exists. Please try another one')
                return render(request, 'profile_edit.html', {'form': form})

            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.username = new_username
            form.save()

            if new_email != user.email:
                request.session['new_email'] = new_email
                return redirect('accounts:verify_email_to_change_email')


            return redirect('accounts:profile')

        form.add_error('email', 'Please enter valid data.')
        return render(request, 'profile_edit.html', {'form': form})

    form = UserProfileModelForm(instance=user)
    data = {
        'form': form
    }
    return render(request, 'profile_edit.html', context=data)


@login_required
@ratelimit(key='user_or_ip', rate='6/m', block=True)
def verify_email_to_change_email(request):
    new_email = request.session.get('new_email')
    if request.method == 'POST':
        errorForm = PassCodeVerification(request.POST)

        if not errorForm.is_valid():
            errorForm.add_error('code', 'Something went wrong.')
            return render(request, 'verify_email_to_change_email.html', {'form': errorForm})

        passcode = request.POST.get('code')

        if not passcode:
            errorForm.add_error('code', 'Please enter a code.')
            return render(request, 'verify_email_to_change_email.html', {'form': errorForm})
        code = CodeEmail.objects.filter(email=new_email).first()

        if not code:
            errorForm.add_error('code', f'Verification code for this email does not exist.')
            return render(request, 'verify_email_to_change_email.html', {'form': errorForm})

        if passcode != code.code_number:
            errorForm.add_error('code', 'Incorrect verification code. Please try again.')
            return render(request, 'verify_email_to_change_email.html', {'form': errorForm})

        if code.expire_date < timezone.now():
            errorForm.add_error('code', 'This code is already expired.')
            return render(request, 'verify_email_to_change_email.html', {'form': errorForm})

        user_db = CustomUser.objects.filter(pk=request.user.pk).update(email=new_email)
        # v2
        # user_db = request.user
        # user_db.email = new_email
        # user_db.save(update_fields=['email'])
        return redirect('accounts:profile')
    if not new_email:
        return HttpResponse('Email not found')

    user_db = CustomUser.objects.filter(pk=request.user.pk).first()
    send_email_to_verify_email(new_email, user_db)
    return render(request, 'verify_email_to_change_email.html')
