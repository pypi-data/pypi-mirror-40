from abc import ABC, abstractmethod

class Model:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():

            if key not in self._accepted_params():
                raise Exception('This model does not allow parameter `' + key + '`')

            setattr(self, key, value)

    @abstractmethod
    def _accepted_params(self):
        pass


    @classmethod
    def from_list(cls, items: list) -> list:
        """
        :param list of dictionaries:
        :return list of models:
        """
        return [cls(**item) for item in items]
