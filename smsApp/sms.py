import africastalking
from django.contrib.auth.mixins import LoginRequiredMixin


# TODO: Initialize Africa's Talking

africastalking.initialize(
    username='PMRA',
    api_key='6fcb1497da1d3536c506162c3b3f9da3082039652ba9ab4b56c2969aaa0c6f30'
    # test env
    # api_key='cc53df940884065d3ef640835a868f52037004f4c67345590aa0712315340f8e'
)


class SendSMS():
    sms = africastalking.SMS
    phone_number = None
    message = None

    def send(self):
        # TODO: Send message

        recipients = self.phone_number
        # Set your message
        message = str(self.message)
        # Set your shortCode or senderId
        sender = 'PMRA'

        try:
            return self.sms.send(message, recipients)
            # return self.sms.send(message, recipients, sender)

        except Exception as e:
            return e
