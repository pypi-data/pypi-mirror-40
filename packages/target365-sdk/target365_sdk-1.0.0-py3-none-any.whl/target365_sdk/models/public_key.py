from .model import Model

class PublicKey(Model):

    def _accepted_params(self) -> list:
        return [
            'accountId',
            'name',
            'expiry',
            'signAlgo',
            'hashAlgo',
            'publicKeyString',
            'notUsableBefore',
            'created',
            'lastModified',
        ]
