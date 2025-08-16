from abc import ABC, abstractmethod
import json

class Account(ABC):
    def __init__(self, balance: float = 0.):
        self._balance = balance

    @abstractmethod
    def make_deposit(self, amount: float) -> None:
        """ Пополнение счета """
        pass
    
    @abstractmethod
    def withdraw_money(self, amount: float) -> None:
        """ Снятие средств со счета """
        pass

    @abstractmethod
    def get_balance(self) -> float:
        return self._balance
    
class LoggingMixin():
    def log(self, message: str) -> str:
        print(f'[Log] {message}')

class SerializableMixin():
    """ Сохранение и загрузка данных в JSON """
    def to_json(self) -> str:
        return json.dumps(self.__dict__)

class SavingsAccount(Account, LoggingMixin, SerializableMixin):
    def make_deposit(self, amount):
        self._balance += amount
        self.log(f'Пополнение {amount}. Текущий баланс: {self._balance}')

    def withdraw_money(self, amount):
        if amount > self._balance:
            raise ValueError("Ошибка, недостаточно средств")
        self._balance -= amount
        self.log(f'Снятие {amount}. Текущий баланс: {self._balance}')

    def get_balance(self):
        return super().get_balance()
    
    def add_percent(self, percent: float = 5.):
        self._balance *= 1 + percent / 100
        self.log(f'Добавлен процент на остаток. Текущий баланс: {self._balance}')

class CreditAccount(Account, LoggingMixin, SerializableMixin):

    def __init__(self, balance: float = 0. , limit = -10000):
        self._limit = limit
        super().__init__(balance)

    def make_deposit(self, amount):
        self._balance += amount
        self.log(f'Пополнение {amount}. Текущий баланс: {self._balance}')

    def withdraw_money(self, amount):
        self._balance -= amount
        if self._limit > self._balance:
            self._balance -= amount * 0.1
        self.log(f'Снятие {amount}. Текущий баланс: {self._balance}')

    def get_balance(self):
        return super().get_balance()
    
if __name__ == '__main__':

    savings = CreditAccount(1000.0)
    savings.make_deposit(500.0)  # Баланс: 1500.0
    savings.withdraw_money(200.0)  # Баланс: 1300.0
    savings.withdraw_money(100000.0)
    json_data = savings.to_json()
    print(json_data) 

