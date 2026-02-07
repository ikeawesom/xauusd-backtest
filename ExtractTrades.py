import csv

class ExtractTrades:
    def __init__(self, src):
        self.df = {}
        with open(src, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
        
            # Date, Open, High, Low, Close, Volume
            next(reader, None)
            
            for row in reader:
                date = self.getDateStr(row[0])
                data = {}
                data["time"] = self.getTimeStr(row[0])
                data["open_price"] = row[1]
                data["high"] = row[2]
                data["low"] = row[3]
                data["close"] = row[4]
                data["change"] = round(float(row[1]) - float(row[4]),2)
                
                if date in self.df:
                    self.df[date].insert(0, data)
                else:
                    self.df[date] = [data]
                    
            self.df = dict(reversed(list(self.df.items())))
            first_key = next(iter(self.df))

            # delete the first key as it has no previous day to compare to
            del self.df[first_key]

    def isBullishDailyBias(self, date): # true is bullish, false is bearish
        prices = self.df[date]
        total = 0
        for price in prices:
            total += float(price["change"])
            
        return total >= 0
        
    def getPDH(self, date):    
        high = -1
        for price in self.df[date]:
            high = max(high, float(price["high"]))

        return high

    def getPDL(self, date):
        low = 9999
        for price in self.df[date]:
            low = min(low, float(price["low"]))

        return low
    
    def displayData(self):
        for date in self.df:
            for prices in self.df[date]:
                print(f"{date}: {prices}")

    def getDf(self):
        return self.df

    def getDateStr(self, s):
        return s.split(" ")[0]

    def getTimeStr(self, s):
        return s.split(" ")[1]