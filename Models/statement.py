from datetime import datetime

class Statement():
    def __init__(self, date, amount, number):
        self.date: datetime = date
        self.amount: int = amount
        self.number: str = number
