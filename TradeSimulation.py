from ExtractTrades import ExtractTrades

class TradeSimulation:
    def __init__(self, src):
        data = ExtractTrades(src)
        self.data = data
        self.df = data.getDf()
        self.results = {}
        self.log = False
        self.winrate = 0
        self.trades_taken = 0
        # print(data.displayData())

    def start(self):
        df = self.data
        initial = True
        prevDate = ""

        for date in self.df:
            if initial:
                prevDate = date
                initial = False
                continue

            if self.log:
                print(f"Analysing previous day stats for {date}...")

            prevDayBias = df.isBullishDailyBias(prevDate)
            PDL = df.getPDL(prevDate)
            PDH = df.getPDH(prevDate)

            if self.log:
                print("="*30)
                print(f"Daily Bias: {"BULLISH" if prevDayBias else "BEARISH"}")
                print(f"PDH: {PDH}")
                print(f"PDL: {PDL}")
                print("="*30)

            prevDate = date

            final_price = -1
            isEntry = False
            isWin = False
            isBE = False
            sweeped = False
            sweeped_price = -1
            entry_price = -1
            exit_price = -1
            entry_time = ""
            time = ""

            self.results[date] = []
            
            for prices in self.df[date]:
                cur_price = float(prices["open_price"])
                time = prices["time"]
                
                if self.log:
                    print(f"{time} Current Price: {cur_price} vs {f"L: {PDL}" if prevDayBias else f"H: {PDH}"}")
                    
                final_price = cur_price
                if isEntry:
                    if prevDayBias and cur_price >= sweeped_price or not(prevDayBias) and cur_price <= sweeped_price:
                        if cur_price == sweeped_price:
                            isBE = True
                            isWin = False
                        else:                           
                            isWin = True

                            temp = {}
                            temp["entry_time"] = entry_time
                            temp["exit_time"] = time
                            temp["bias"] = "BULLISH" if prevDayBias else "BEARISH"
                            temp["is_win"] = "BE" if isBE else "WIN" if isWin else "LOSE"
                            temp["entry_price"] = entry_price
                            temp["exit_price"] = cur_price

                            if self.log:
                                print("="*30)
                                print("Trade WON")
                                print("Trade Details:", temp)
                                print("="*30)
                            
                            self.results[date].append(temp)

                            final_price = -1
                            isEntry = False
                            isWin = False
                            isBE = False
                            sweeped = False
                            sweeped_price = -1
                            entry_price = -1
                            entry_time = ""
                            
                        exit_price = cur_price
                    else:
                        # hit stop loss
                        isWin = False
                        exit_price = cur_price
                        break
                else:
                    if not(sweeped):
                        if prevDayBias and cur_price <= PDL or not(prevDayBias) and cur_price >= PDH:
                            # sweep low/high
                            if self.log:
                                print("="*30)
                                print(f"Price manage to sweep {f"L: {PDL}" if prevDayBias else f"H: {PDH}"}")
                                print("="*30)
                            sweeped = True
                            sweeped_price = cur_price
                            continue
                        if self.log:
                            print(f"Price did not sweep {f"L: {PDL}" if prevDayBias else f"H: {PDH}"}")
                    else:
                        if prevDayBias and cur_price >= sweeped_price or not(prevDayBias) and cur_price <= sweeped_price:
                            # enter
                            if self.log:
                                print(f"Price swept and is reversing: {cur_price}")
                            isEntry = True
                            entry_price = cur_price
                            entry_time = time
                            if self.log:
                                print(f"ENTRY AT: {entry_price}")
                        else:
                            if self.log:
                                print(f"Price swept and is not reversing: {cur_price}")
                            sweeped_price = cur_price 
            
            if not(isEntry):
                if len(self.results[date]) == 0:
                    self.results[date] = "NO TRADE"
                if self.log:
                    print(f"NO TRADE on {date}\n")
                continue

            if exit_price == -1:
                # did not finish
                if prevDayBias and final_price >= entry_price or not(prevDayBias) and final_price <= entry_price:
                    isWin = True
                    exit_price = final_price

            if self.log:
                print("EXIT AT:", exit_price)

            if entry_price == exit_price:
                isBE = True
                    
            temp = {}
            temp["entry_time"] = entry_time
            temp["exit_time"] = time
            temp["bias"] = "BULLISH" if prevDayBias else "BEARISH"
            temp["is_win"] = "BE" if isBE else "WIN" if isWin else "LOSE"
            temp["entry_price"] = entry_price
            temp["exit_price"] = cur_price
            
            self.results[date].append(temp)

    def calculateResults(self):
        count = 0
        wins = 0
        for date in self.results:
            if self.results[date] != "NO TRADE":
                count += len(self.results[date])
                for trades in self.results[date]:
                    if trades["is_win"] == "WIN":
                        wins += 1

        if count == 0:
            return {"trades_taken": 0, "winrate": 0, "wins": 0}
            
        self.trades_taken = count
        self.winrate = round(float(wins)/float(count) * 100, 2)

        return {"trades_taken": self.trades_taken, "winrate": self.winrate, "wins": wins}
        
    def displayResults(self, full = False):
        
        if full:
            for date in self.results:
                trades = self.results[date]
                isNoTrade = trades == "NO TRADE"
                print(f"{"="*10} {date} ({"0" if isNoTrade else len(trades)}) {"="*10}")
                if isNoTrade:
                    print("NO TRADE")
                    continue

                for trade in trades:
                    print(f"{trade["entry_time"]} Entry: {trade["entry_price"]}")
                    print(f"{trade["exit_time"]} Exit: {trade["exit_price"]}")
                    print(f"Result: {trade["is_win"]}")
                    
        print(f"{"="*30} Overall Statistics {"="*30}")

        results = self.calculateResults()
        
        print(f"Trades taken: {results["trades_taken"]}")
        print(f"Win rate: {results["winrate"]}%")

        print("="*80)

    def enableLog(self):
        self.log = True

    def disableLog(self):
        self.log = False