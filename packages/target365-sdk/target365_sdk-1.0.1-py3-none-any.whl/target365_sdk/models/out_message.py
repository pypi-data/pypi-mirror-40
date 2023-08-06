from .model import Model

class OutMessage(Model):


    def _accepted_params(self):
        return [
            'id',
            'accountId',
            'transactionId',
            'sender',
            'recipient',
            'content',
            'sendTime',
            'timeToLive',
            'priority',
            'deliveryMode',

            # only used for STREX messages
            'merchantId',
            'serviceCode',
            'invoiceText',
            'price',

            'lastModified',
            'created',
            'statusCode',
            'delivered',
            'billed',
            'tags',
            'properties',

            'eTag',
            'proxyETag',
            'subMessageInfos',
            'PartitionKey',
        ]
