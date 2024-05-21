from twilio.rest import Client
from django.conf import settings

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN

class SendSMS:
    user = None

    def __init__(self, user):
        self.user = user

    def send_message(self):
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body=f"Your OTP is {self.user.user_otp}",
                from_='+16502274525',
                to=F'+91{self.user.phone_number}'
            )

        print(message)

