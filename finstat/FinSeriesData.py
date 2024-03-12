import datetime

class FinSeriesData:
    def __init__(self):
        self.dates  : list[datetime.datetime] = [] 
        self.values = []

    def add(self, date, value):
        self.dates.append(date)
        self.values.append(value)
    
    def add_range(self, dates, values):
        self.dates.extend(dates)
        self.values.extend(values)
    def sort(self):
        self.dates, self.values 