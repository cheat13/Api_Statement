from datetime import datetime

class Statement():
    def __init__(self, date, amount, number):
        self.date: datetime = date
        self.amount: float = amount
        self.number: str = number
