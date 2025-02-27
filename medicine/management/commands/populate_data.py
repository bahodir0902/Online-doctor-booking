from datetime import datetime, time
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_datetime
from medicine.models import (
    User,
    Department,
    Doctor,
    Appointment,
    Notification,
    Feedback,
    Availability,
)

class Command(BaseCommand):
    help = 'Populate the database with initial realistic data.'

    def handle(self, *args, **options):
        self.stdout.write("Starting data population...")
        self.populate_data()
        self.stdout.write("Data population complete!")

    def populate_data(self):
        with transaction.atomic():
            # Create Users (first 10 are patients; next 10 are doctors)
            user_data = [
                # Patients
                User(first_name='John', last_name='Doe', email='johndoe@example.com', phone_number='555-1234', username='johndoe', password='password1', is_active=True, is_doctor=False),
                User(first_name='Jane', last_name='Smith', email='janesmith@example.com', phone_number='555-5678', username='janesmith', password='password2', is_active=True, is_doctor=False),
                User(first_name='Michael', last_name='Johnson', email='michael.j@example.com', phone_number='555-8765', username='mjohnson', password='password3', is_active=True, is_doctor=False),
                User(first_name='Emily', last_name='Davis', email='emilyd@example.com', phone_number='555-4321', username='edavis', password='password4', is_active=True, is_doctor=False),
                User(first_name='Robert', last_name='Brown', email='robert.brown@example.com', phone_number='555-2345', username='rbrown', password='password5', is_active=True, is_doctor=False),
                User(first_name='Linda', last_name='Wilson', email='linda.w@example.com', phone_number='555-3456', username='lwilson', password='password6', is_active=True, is_doctor=False),
                User(first_name='David', last_name='Miller', email='david.m@example.com', phone_number='555-4567', username='dmiller', password='password7', is_active=True, is_doctor=False),
                User(first_name='Susan', last_name='Taylor', email='susan.taylor@example.com', phone_number='555-9876', username='staylor', password='password8', is_active=True, is_doctor=False),
                User(first_name='James', last_name='Anderson', email='james.anderson@example.com', phone_number='555-6543', username='janderson', password='password9', is_active=True, is_doctor=False),
                User(first_name='Patricia', last_name='Thomas', email='patricia.thomas@example.com', phone_number='555-3210', username='pthomas', password='password10', is_active=True, is_doctor=False),
                # Doctors
                User(first_name='Alan', last_name='Scott', email='alan.scott@example.com', phone_number='555-1111', username='drascott', password='drpass1', is_active=True, is_doctor=True),
                User(first_name='Brenda', last_name='Lee', email='brenda.lee@example.com', phone_number='555-2222', username='drblee', password='drpass2', is_active=True, is_doctor=True),
                User(first_name='Charles', last_name='King', email='charles.king@example.com', phone_number='555-3333', username='drcking', password='drpass3', is_active=True, is_doctor=True),
                User(first_name='Diana', last_name='Prince', email='diana.prince@example.com', phone_number='555-4444', username='drdprince', password='drpass4', is_active=True, is_doctor=True),
                User(first_name='Edward', last_name='Norton', email='edward.norton@example.com', phone_number='555-5555', username='drenorton', password='drpass5', is_active=True, is_doctor=True),
                User(first_name='Fiona', last_name='Gallagher', email='fiona.g@example.com', phone_number='555-6666', username='drfgallagher', password='drpass6', is_active=True, is_doctor=True),
                User(first_name='George', last_name='Martin', email='george.martin@example.com', phone_number='555-7777', username='drgmartin', password='drpass7', is_active=True, is_doctor=True),
                User(first_name='Hannah', last_name='Baker', email='hannah.baker@example.com', phone_number='555-8888', username='drhbaker', password='drpass8', is_active=True, is_doctor=True),
                User(first_name='Ian', last_name='Wright', email='ian.wright@example.com', phone_number='555-9999', username='driwright', password='drpass9', is_active=True, is_doctor=True),
                User(first_name='Julia', last_name='Roberts', email='julia.roberts@example.com', phone_number='555-0000', username='drjroberts', password='drpass10', is_active=True, is_doctor=True),
            ]
            User.objects.bulk_create(user_data)
            users = list(User.objects.order_by('id'))

            # Create Departments
            department_data = [
                Department(name='Cardiology'),
                Department(name='Neurology'),
                Department(name='Pediatrics'),
                Department(name='Orthopedics'),
                Department(name='Dermatology'),
                Department(name='General Medicine'),
                Department(name='Radiology'),
                Department(name='Gastroenterology'),
                Department(name='Urology'),
                Department(name='Oncology'),
            ]
            Department.objects.bulk_create(department_data)
            departments = list(Department.objects.order_by('id'))

            # Create Doctors (associate doctor records with the doctor users)
            doctor_data = [
                Doctor(user=users[10], department=departments[0], experienced_years=15, biography='Expert cardiologist with over 15 years of experience.'),
                Doctor(user=users[11], department=departments[1], experienced_years=10, biography='Specialist in neurology and brain disorders.'),
                Doctor(user=users[12], department=departments[2], experienced_years=8, biography='Dedicated pediatrician focused on child health.'),
                Doctor(user=users[13], department=departments[5], experienced_years=12, biography='Experienced general practitioner with a holistic approach.'),
                Doctor(user=users[14], department=departments[3], experienced_years=20, biography='Orthopedic surgeon with a record of successful surgeries.'),
                Doctor(user=users[15], department=departments[4], experienced_years=7, biography='Dermatologist specialized in skin conditions.'),
                Doctor(user=users[16], department=departments[6], experienced_years=9, biography='Expert radiologist with advanced imaging skills.'),
                Doctor(user=users[17], department=departments[7], experienced_years=11, biography='Gastroenterologist with focus on digestive health.'),
                Doctor(user=users[18], department=departments[8], experienced_years=6, biography='Urologist with emphasis on minimally invasive procedures.'),
                Doctor(user=users[19], department=departments[9], experienced_years=14, biography='Oncologist committed to cancer research and patient care.'),
            ]
            Doctor.objects.bulk_create(doctor_data)
            doctors = list(Doctor.objects.order_by('id'))

            # Create Appointments
            appointment_data = [
                Appointment(datetime=parse_datetime('2023-07-01 09:00:00'), doctor=doctors[0], user=users[0], status='Confirmed'),
                Appointment(datetime=parse_datetime('2023-07-02 10:30:00'), doctor=doctors[1], user=users[1], status='Pending'),
                Appointment(datetime=parse_datetime('2023-07-03 11:15:00'), doctor=doctors[2], user=users[2], status='Completed'),
                Appointment(datetime=parse_datetime('2023-07-04 14:00:00'), doctor=doctors[3], user=users[3], status='Confirmed'),
                Appointment(datetime=parse_datetime('2023-07-05 15:30:00'), doctor=doctors[4], user=users[4], status='Canceled'),
                Appointment(datetime=parse_datetime('2023-07-06 09:45:00'), doctor=doctors[5], user=users[5], status='Pending'),
                Appointment(datetime=parse_datetime('2023-07-07 10:00:00'), doctor=doctors[6], user=users[6], status='Confirmed'),
                Appointment(datetime=parse_datetime('2023-07-08 11:30:00'), doctor=doctors[7], user=users[7], status='Completed'),
                Appointment(datetime=parse_datetime('2023-07-09 12:15:00'), doctor=doctors[8], user=users[8], status='Confirmed'),
                Appointment(datetime=parse_datetime('2023-07-10 13:00:00'), doctor=doctors[9], user=users[9], status='Pending'),
                Appointment(datetime=parse_datetime('2023-07-11 09:15:00'), doctor=doctors[0], user=users[1], status='Completed'),
                Appointment(datetime=parse_datetime('2023-07-12 10:45:00'), doctor=doctors[1], user=users[2], status='Confirmed'),
                Appointment(datetime=parse_datetime('2023-07-13 11:00:00'), doctor=doctors[2], user=users[3], status='Canceled'),
                Appointment(datetime=parse_datetime('2023-07-14 14:30:00'), doctor=doctors[3], user=users[4], status='Pending'),
                Appointment(datetime=parse_datetime('2023-07-15 15:00:00'), doctor=doctors[4], user=users[5], status='Confirmed'),
                Appointment(datetime=parse_datetime('2023-07-16 09:30:00'), doctor=doctors[5], user=users[6], status='Completed'),
                Appointment(datetime=parse_datetime('2023-07-17 10:15:00'), doctor=doctors[6], user=users[7], status='Pending'),
                Appointment(datetime=parse_datetime('2023-07-18 11:45:00'), doctor=doctors[7], user=users[8], status='Confirmed'),
                Appointment(datetime=parse_datetime('2023-07-19 12:30:00'), doctor=doctors[8], user=users[9], status='Completed'),
                Appointment(datetime=parse_datetime('2023-07-20 13:15:00'), doctor=doctors[9], user=users[0], status='Confirmed'),
            ]
            Appointment.objects.bulk_create(appointment_data)
            appointments = list(Appointment.objects.order_by('id'))

            # Create Notifications
            notification_data = [
                Notification(title='Appointment Reminder', content='Your appointment with Dr. Alan Scott is scheduled for 2023-07-01 09:00:00.', is_read=False, user=users[0], created_at=parse_datetime('2023-06-30 08:00:00')),
                Notification(title='Appointment Confirmation', content='Your appointment with Dr. Brenda Lee has been confirmed.', is_read=True, user=users[1], created_at=parse_datetime('2023-07-01 10:00:00')),
                Notification(title='Appointment Completed', content='Your appointment with Dr. Charles King has been completed.', is_read=False, user=users[2], created_at=parse_datetime('2023-07-03 12:00:00')),
                Notification(title='Appointment Canceled', content='Your appointment with Dr. Diana Prince has been canceled.', is_read=False, user=users[3], created_at=parse_datetime('2023-07-04 13:00:00')),
                Notification(title='New Message', content='Please contact our office regarding your appointment.', is_read=False, user=users[4], created_at=parse_datetime('2023-07-05 08:30:00')),
                Notification(title='Feedback Request', content='Please provide feedback for your recent visit.', is_read=False, user=users[5], created_at=parse_datetime('2023-07-06 10:00:00')),
                Notification(title='Appointment Reminder', content='Reminder: Your appointment is tomorrow.', is_read=True, user=users[6], created_at=parse_datetime('2023-07-06 18:00:00')),
                Notification(title='Health Tips', content='Remember to stay hydrated and exercise regularly.', is_read=False, user=users[7], created_at=parse_datetime('2023-07-07 09:15:00')),
                Notification(title='Appointment Rescheduled', content='Your appointment has been rescheduled to 2023-07-09 12:15:00.', is_read=False, user=users[8], created_at=parse_datetime('2023-07-08 11:00:00')),
                Notification(title='Prescription Ready', content='Your prescription is ready for pickup.', is_read=False, user=users[9], created_at=parse_datetime('2023-07-09 14:00:00')),
                Notification(title='Follow-up Reminder', content='Please schedule a follow-up appointment if needed.', is_read=False, user=users[0], created_at=parse_datetime('2023-07-10 09:30:00')),
                Notification(title='Lab Results', content='Your lab results are now available.', is_read=True, user=users[1], created_at=parse_datetime('2023-07-10 15:45:00')),
                Notification(title='Billing Notice', content='Your billing statement is ready.', is_read=False, user=users[2], created_at=parse_datetime('2023-07-11 10:20:00')),
                Notification(title='Appointment Reminder', content='Your appointment with Dr. Diana Prince is coming up.', is_read=True, user=users[3], created_at=parse_datetime('2023-07-12 08:50:00')),
                Notification(title='New Health Article', content='Check out our new article on heart health.', is_read=False, user=users[4], created_at=parse_datetime('2023-07-12 12:30:00')),
            ]
            Notification.objects.bulk_create(notification_data)

            # Create Feedbacks
            feedback_data = [
                Feedback(content='Excellent care, very satisfied.', rate=5, appointment_id=appointments[2], created_at=parse_datetime('2023-07-03 13:00:00')),
                Feedback(content='Very professional and kind.', rate=4, appointment_id=appointments[3], created_at=parse_datetime('2023-07-04 15:00:00')),
                Feedback(content='Quick and efficient service.', rate=4, appointment_id=appointments[6], created_at=parse_datetime('2023-07-07 11:00:00')),
                Feedback(content='Average experience.', rate=3, appointment_id=appointments[9], created_at=parse_datetime('2023-07-10 14:00:00')),
                Feedback(content='Not satisfied with the waiting time.', rate=2, appointment_id=appointments[18], created_at=parse_datetime('2023-07-19 13:00:00')),
            ]
            Feedback.objects.bulk_create(feedback_data)

            # Create Availabilities for each doctor
            availability_data = [
                # Doctor 1: Alan Scott
                Availability(doctor=doctors[0], start_time=time(9, 0), end_time=time(12, 0), days_of_week='Monday'),
                Availability(doctor=doctors[0], start_time=time(13, 0), end_time=time(17, 0), days_of_week='Wednesday'),
                Availability(doctor=doctors[0], start_time=time(9, 0), end_time=time(12, 0), days_of_week='Friday'),
                # Doctor 2: Brenda Lee
                Availability(doctor=doctors[1], start_time=time(10, 0), end_time=time(14, 0), days_of_week='Monday'),
                Availability(doctor=doctors[1], start_time=time(10, 0), end_time=time(14, 0), days_of_week='Wednesday'),
                Availability(doctor=doctors[1], start_time=time(10, 0), end_time=time(14, 0), days_of_week='Friday'),
                # Doctor 3: Charles King
                Availability(doctor=doctors[2], start_time=time(8, 0), end_time=time(11, 0), days_of_week='Monday'),
                Availability(doctor=doctors[2], start_time=time(8, 0), end_time=time(11, 0), days_of_week='Wednesday'),
                Availability(doctor=doctors[2], start_time=time(8, 0), end_time=time(11, 0), days_of_week='Friday'),
                # Doctor 4: Diana Prince
                Availability(doctor=doctors[3], start_time=time(12, 0), end_time=time(16, 0), days_of_week='Monday'),
                Availability(doctor=doctors[3], start_time=time(12, 0), end_time=time(16, 0), days_of_week='Wednesday'),
                Availability(doctor=doctors[3], start_time=time(12, 0), end_time=time(16, 0), days_of_week='Friday'),
                # Doctor 5: Edward Norton
                Availability(doctor=doctors[4], start_time=time(9, 30), end_time=time(12, 30), days_of_week='Monday'),
                Availability(doctor=doctors[4], start_time=time(9, 30), end_time=time(12, 30), days_of_week='Wednesday'),
                Availability(doctor=doctors[4], start_time=time(9, 30), end_time=time(12, 30), days_of_week='Friday'),
                # Doctor 6: Fiona Gallagher
                Availability(doctor=doctors[5], start_time=time(11, 0), end_time=time(15, 0), days_of_week='Monday'),
                Availability(doctor=doctors[5], start_time=time(11, 0), end_time=time(15, 0), days_of_week='Wednesday'),
                Availability(doctor=doctors[5], start_time=time(11, 0), end_time=time(15, 0), days_of_week='Friday'),
                # Doctor 7: George Martin
                Availability(doctor=doctors[6], start_time=time(10, 30), end_time=time(13, 30), days_of_week='Monday'),
                Availability(doctor=doctors[6], start_time=time(10, 30), end_time=time(13, 30), days_of_week='Wednesday'),
                Availability(doctor=doctors[6], start_time=time(10, 30), end_time=time(13, 30), days_of_week='Friday'),
                # Doctor 8: Hannah Baker
                Availability(doctor=doctors[7], start_time=time(8, 30), end_time=time(12, 30), days_of_week='Monday'),
                Availability(doctor=doctors[7], start_time=time(8, 30), end_time=time(12, 30), days_of_week='Wednesday'),
                Availability(doctor=doctors[7], start_time=time(8, 30), end_time=time(12, 30), days_of_week='Friday'),
                # Doctor 9: Ian Wright
                Availability(doctor=doctors[8], start_time=time(14, 0), end_time=time(18, 0), days_of_week='Monday'),
                Availability(doctor=doctors[8], start_time=time(14, 0), end_time=time(18, 0), days_of_week='Wednesday'),
                Availability(doctor=doctors[8], start_time=time(14, 0), end_time=time(18, 0), days_of_week='Friday'),
                # Doctor 10: Julia Roberts
                Availability(doctor=doctors[9], start_time=time(9, 0), end_time=time(11, 0), days_of_week='Monday'),
                Availability(doctor=doctors[9], start_time=time(9, 0), end_time=time(11, 0), days_of_week='Wednesday'),
                Availability(doctor=doctors[9], start_time=time(9, 0), end_time=time(11, 0), days_of_week='Friday'),
            ]
            Availability.objects.bulk_create(availability_data)