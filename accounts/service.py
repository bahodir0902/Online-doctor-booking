from .utils import generate_random_code
from django.core.mail import EmailMultiAlternatives
from threading import Thread
from .models import CodePassword, CodeEmail


def send_email_verification(receiver_email, first_name):
    code = generate_random_code()
    CodeEmail.objects.create(code_number=code, email=receiver_email)
    subject = ''
    text_content = f'''
    Hello {first_name},

    Thank you for signing up! To secure your account, please verify your email address.

    Your 4-digit verification code is: {code}

    Enter this code on our website to complete the verification process.

    If you didn’t request this, please ignore this email.

    Best regards,  
    Your Company Team
    '''

    from_email = 'vbahodir00@gmail.com'
    to = [receiver_email]
    html_content = f"""
        <div style="font-family: 'Helvetica Neue', Arial, sans-serif; background: #f9f9f9; padding: 40px 20px;">
          <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #6D5DF6, #1E90FF); padding: 20px; text-align: center;">
              <h1 style="color: #fff; margin: 0; font-size: 28px;">Verify Your Email 🚀</h1>
            </div>
            <!-- Main Content -->
            <div style="padding: 30px; text-align: center;">
              <p style="color: #555; font-size: 16px; margin-bottom: 20px;">
                You're just one step away from activating your account!
              </p>
              <div style="background: #F4F8FF; border-radius: 8px; padding: 15px 20px; display: inline-block; margin-bottom: 20px;">
                <span style="color: #1E90FF; font-size: 20px; font-weight: bold;">Your Verification Code:</span>
                <div style="color: #6D5DF6; font-size: 36px; font-weight: bold; margin-top: 10px;">
                  {code}
                </div>
              </div>
              <p style="color: #555; font-size: 16px; margin-bottom: 30px;">
                Enter this code on our website to complete the verification process.
              </p>
            </div>
            <!-- Footer -->
            <div style="background: #f1f1f1; padding: 15px 20px; text-align: center;">
              <p style="color: #888; font-size: 12px; margin: 0;">
                If you didn’t request this email, please ignore it.
              </p>
              <p style="color: #888; font-size: 12px; margin: 5px 0 0;">
                Need help? <a href="mailto:support@yourcompany.com" style="color: #1E90FF; text-decoration: none;">Contact our support team</a>.
              </p>
              <p style="color: #888; font-size: 12px; margin: 15px 0 0;">
                Best regards,<br>
                <strong>Your Company Team</strong>
              </p>
            </div>
          </div>
        </div>
        """

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')

    thread1 = Thread(target=email.send)
    thread1.start()
    # email.send()


def send_password_verification(user):
    subject = 'Password reset request'
    code = generate_random_code()
    CodePassword.objects.create(code_number=code, user_id=user.id)
    to = [user.email]
    from_email = 'vbahodir00@gmail.com'
    text_content = f'''
    Hello {user.first_name},

    Thank you for signing up! To secure your account, please verify your email address.

    Your 4-digit verification code is: {code}

    Enter this code on our website to complete the verification process.

    If you didn’t request this, please ignore this email.

    Best regards,  
    Your Company Team
    '''

    html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #333;">Hello, {user.first_name} 👋</h2>
            <p style="color: #555; font-size: 16px;">
                We received a request to verify your email address.
            </p>
            <p style="color: #333; font-size: 18px; font-weight: bold; text-align: center;">
                Your 4-digit passcode: <span style="color: #007BFF;">{code}</span>
            </p>
            <p style="color: #555; font-size: 16px;">
                Enter this code on the website to complete your verification.
            </p>
            <p style="color: #777; font-size: 14px;">
                If you didn’t request this, you can safely ignore this email.
            </p>
            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <p style="color: #888; font-size: 12px;">
                If you need help, please contact our support team.
            </p>
            <p style="color: #888; font-size: 12px;">
                Best regards, <br>
                <strong>Your Company Team</strong>
            </p>
        </div>
        """

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')

    thread1 = Thread(target=email.send)
    thread1.start()
    # email.send()


def send_email_to_verify_email(receiver_new_email, user):
    subject = 'Confirm Your New Email Address'
    code = generate_random_code()
    CodeEmail.objects.create(code_number=code, email=receiver_new_email)

    from_email = 'vbahodir00@gmail.com'
    to = [receiver_new_email]

    text_content = f'''
        Hello {user.first_name},

        You've requested to change your email address associated with your account. 

        To verify your new email, please enter the following 4-digit verification code:

        {code}

        If you didn’t request this change, please ignore this email.

        Best regards,  
        Your Company Team
        '''

    html_content = f"""
            <div style="font-family: 'Helvetica Neue', Arial, sans-serif; background: #f9f9f9; padding: 40px 20px;">
              <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #6D5DF6, #1E90FF); padding: 20px; text-align: center;">
                  <h1 style="color: #fff; margin: 0; font-size: 24px;">Confirm Your New Email Address</h1>
                </div>
                <!-- Main Content -->
                <div style="padding: 30px; text-align: center;">
                  <p style="color: #555; font-size: 16px; margin-bottom: 20px;">
                    You've requested to update your email address. To proceed, please enter the following code:
                  </p>
                  <div style="background: #F4F8FF; border-radius: 8px; padding: 15px 20px; display: inline-block; margin-bottom: 20px;">
                    <span style="color: #1E90FF; font-size: 20px; font-weight: bold;">Your Verification Code:</span>
                    <div style="color: #6D5DF6; font-size: 36px; font-weight: bold; margin-top: 10px;">
                      {code}
                    </div>
                  </div>
                  <p style="color: #555; font-size: 16px; margin-bottom: 30px;">
                    Enter this code on our website to verify your new email.
                  </p>
                </div>
                <!-- Footer -->
                <div style="background: #f1f1f1; padding: 15px 20px; text-align: center;">
                  <p style="color: #888; font-size: 12px; margin: 0;">
                    If you didn’t request this email change, you can ignore this email.
                  </p>
                  <p style="color: #888; font-size: 12px; margin: 5px 0 0;">
                    Need help? <a href="mailto:support@yourcompany.com" style="color: #1E90FF; text-decoration: none;">Contact our support team</a>.
                  </p>
                  <p style="color: #888; font-size: 12px; margin: 15px 0 0;">
                    Best regards,<br>
                    <strong>Your Company Team</strong>
                  </p>
                </div>
              </div>
            </div>
        """

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')

    thread1 = Thread(target=email.send)
    thread1.start()


def send_congratulations_email(receiver_email, first_name):
    subject = 'Congratulations on Your Registration 🎉'

    text_content = f'''
    Hello {first_name},

    Congratulations on successfully registering with us!

    We're thrilled to welcome you to our community. Explore our platform and enjoy the exclusive benefits waiting for you.

    If you have any questions, feel free to reach out to our support team.

    Warm regards,
    Your Company Team
    '''

    from_email = 'vbahodir00@gmail.com'
    to = [receiver_email]

    html_content = f"""
        <div style="font-family: 'Helvetica Neue', Arial, sans-serif; background: #e0f7fa; padding: 40px 20px;">
          <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #ff4081, #f50057); padding: 20px; text-align: center;">
              <h1 style="color: #fff; margin: 0; font-size: 32px;">Congratulations! 🎉</h1>
            </div>
            <!-- Main Content -->
            <div style="padding: 30px; text-align: center;">
              <p style="color: #333; font-size: 18px; margin-bottom: 20px;">
                Hello {first_name}, welcome to our community!
              </p>
              <p style="color: #555; font-size: 16px; margin-bottom: 30px;">
                Your registration was successful. We are excited to have you with us. Dive in and explore the exclusive benefits we offer.
              </p>
              <a href="https://yourwebsite.com" style="background: linear-gradient(135deg, #ff4081, #f50057); color: #fff; padding: 15px 30px; border-radius: 5px; text-decoration: none; font-size: 16px;">
                Get Started
              </a>
            </div>
            <!-- Footer -->
            <div style="background: #f1f1f1; padding: 15px 20px; text-align: center;">
              <p style="color: #888; font-size: 12px; margin: 0;">
                If you have any questions, feel free to <a href="mailto:support@yourcompany.com" style="color: #f50057; text-decoration: none;">contact our support team</a>.
              </p>
              <p style="color: #888; font-size: 12px; margin: 5px 0 0;">
                Best regards,<br>
                <strong>Your Company Team</strong>
              </p>
            </div>
          </div>
        </div>
        """

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, 'text/html')

    thread1 = Thread(target=email.send)
    thread1.start()