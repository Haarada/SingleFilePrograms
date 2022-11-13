#import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime as dt

class DataFragment:
    def __init__(self, category: str, name: str, percentage: float):
        self.category = category
        self.name = name
        self.percentage = percentage


class DatePoint:
    def __init__(self, date: dt.date):
        self.date = date
        self.data = []

    def addData(self, data: DataFragment):
        self.data.append(data)
    
    def deleteDataAtIndex(self, index: int):
        self.data.pop(index)


class DateContainer:
    def __init__(self):
        self.dates = []

    def addDate(self, date: DatePoint):
        self.dates.append(date)
    
    def deleteDateAtIndex(self, index: int):
        self.dates.pop(index)



if __name__ == "__main__":
    dc = DateContainer()
    
    with open(r"../../Data/shs.csv") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        next(csvreader)
        for row in csvreader:
            if len(dc.dates) == 0:
                dc.addDate(DatePoint( dt.strptime(row[0],"%Y-%m-%d").date() ))
                print(dc.dates[0].date)
                exit()