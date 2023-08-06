from .model import Model

class StrexTransaction(Model):

    def _accepted_params(self):
        return [
            'transactionId',
            'invoiceText',
            'lastModified',
            'merchantId',
            'price',
            'recipient',
            'serviceCode',
            'shortNumber',
            'created',

            'deliveryMode',
            'statusCode',
            'accountId',
            'strexOtpTransactionId',
            'smscTransactionId',
            'eTag',
            'billed',
        ]

