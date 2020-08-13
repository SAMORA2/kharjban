class Person:
    def __init__(self, id, name, balance: str):
        self.id = id
        self.name = name
        self.balance = balance

    def get_balance(self):
        return self.balance

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_balance(self, balance):
        self.balance = balance


class Expense(Person):

    def __init__(self, id, name, balance, category, cost, date):
        super().__init__(id, name, balance)
        self.category = category
        self.cost = cost
        self.date = date

    def spend(self):
        self.balance = int(self.balance) - int(self.cost)
        return self.balance
