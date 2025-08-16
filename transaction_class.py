import datetime

class Transaction:
    def __init__(self, type: str, amount: float):
        self._type = type
        self._amount = amount
        self._datetime = datetime.datetime.now()

    def to_dict(self):
        return {
            'type': self._type, 
            'amount': self._amount, 
            'datetime': self._datetime
        }

    def __str__(self):
        return f'Тип операции: {self._type}, сумма операции: {self._amount}, время операции: {self._datetime}'
    
    def __repr__(self):
        return f'{self.__class__.__name__}: type({self._type}), amount({self._amount}), datetime({self._datetime})'
