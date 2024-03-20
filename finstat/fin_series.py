class FinSeries:
    def __init__(self):
        self.__data = []

    def addData(self, data):
        self.__data.append(data)

    def getData(self):
        return self.__data
