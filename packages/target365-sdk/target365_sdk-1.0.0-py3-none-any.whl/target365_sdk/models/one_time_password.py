from .model import Model

class OneTimePassword(Model):

    def _accepted_params(self) -> list:
        return [
            'transactionId',
            'merchantId',
            'recipient',
            'sender',
            'recurring',
            'message',
            'timeToLive',
            'created',
            'delivered',
        ]
