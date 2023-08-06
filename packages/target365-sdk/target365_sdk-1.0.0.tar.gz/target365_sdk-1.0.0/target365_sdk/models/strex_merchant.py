from .model import Model

class StrexMerchant(Model):

    def _accepted_params(self) -> list:
        return [
            'merchantId',
            'shortNumberId',
            'password',
        ]
