from abc import ABC, abstractmethod
from transaction_class import Transaction
from functools import wraps
import datetime
import json  

class AccountABC(ABC):
             
    @abstractmethod
    def make_deposit(self):
        pass
    
    @abstractmethod
    def withdraw_money(self):
        pass

    @abstractmethod
    def get_balance(self):
        pass

class Account(AccountABC):
    def __init__(self, balance: float = 0.):
        self._balance: float = balance
        self._transactions_list: list[Transaction] = []


    def log_transaction(transaction_type: str):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                transaction_amount = kwargs.get('amount')
                if transaction_amount is None:
                    param_names = func.__code__.co_varnames[1:]
                    for name, arg in zip(param_names, args):
                        if name == 'amount':
                            transaction_amount = arg
                            break
                if transaction_amount is None:
                    raise ValueError('Не удалось найти параметр amount.')
                res = func(self, *args, **kwargs)
                self._transactions_list.append(
                    Transaction(
                        type = transaction_type, 
                        amount=transaction_amount,
                        ))
                return res
            return wrapper
        return decorator
             
    @log_transaction(transaction_type='DEPOSIT')
    def make_deposit(self, amount):
        self._balance += amount
        self.log(f'Пополнение {amount}. Текущий баланс: {self._balance}')

    def get_balance(self) -> float:
        return self._balance
    
    def get_all_transactions(self) -> None:
        for transaction in self._transactions_list:
            print(transaction)
    
class LoggingMixin():
    def log(self, message: str) -> None:
        print(f'[Log] {message}')

class SerializableMixin():
    """ Сохранение и загрузка данных в JSON """
    def to_json(self) -> str:
        def convert_obj(obj):
            if hasattr(obj, 'to_dict'):
                return obj.to_dict()
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat()
            return str(obj)

        data = {k: convert_obj(v) for k, v in self.__dict__.items()}
        
        return json.dumps(data, indent=2)

class SavingsAccount(Account, LoggingMixin, SerializableMixin):
    @Account.log_transaction(transaction_type='WITHDRAW')
    def withdraw_money(self, amount):
        if amount > self._balance:
            raise ValueError("Ошибка, недостаточно средств")
        self._balance -= amount
        self.log(f'Снятие {amount}. Текущий баланс: {self._balance}')
    
    def add_percent(self, percent: float = 5.):
        self._balance *= 1 + percent / 100
        self.log(f'Добавлен процент на остаток. Текущий баланс: {self._balance}')

class CreditAccount(Account, LoggingMixin, SerializableMixin):
    def __init__(self, balance: float = 0. , limit = -10000):
        self._limit = limit
        super().__init__(balance)

    @Account.log_transaction(transaction_type='WITHDRAW')
    def withdraw_money(self, amount):
        new_balance = self._balance - amount
        if new_balance < self._limit:
            fee = amount * 0.1
            amount += fee
        self._balance -= amount
        self.log(f'Снятие {amount}. Текущий баланс: {self._balance}')
        
if __name__ == '__main__':

    savings = SavingsAccount(1000.0)
    savings.make_deposit(500.0)  # Баланс: 1500.0
    savings.withdraw_money(200.0)  # Баланс: 1300.0
    savings.withdraw_money(100.0)
    savings.add_percent()
    savings.get_all_transactions()
