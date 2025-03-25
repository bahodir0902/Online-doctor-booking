from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import CustomUser
from accounts.service import send_congratulations_email

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created: # created
        print('Hello new User!')
        send_congratulations_email(instance.email, instance.first_name)
    # if not created -> updated

# @receiver(pre_save, sender=CustomUser)
