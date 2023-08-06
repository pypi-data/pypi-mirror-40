from .model import Model

class InMessage(Model):


    def _accepted_params(self) -> list:

        return [
            'messageId',
            'transactionId',
            'processed',
            'processAttempts',
            'sender',
            'recipient',
            'content',
            'keywordId',
            'isStopMessage',
            'created',
            'properties',
            'tags',
            'eTag',
        ]
