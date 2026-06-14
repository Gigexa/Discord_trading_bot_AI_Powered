import yfinance as yf
import traceback
import pandas as pd



class Analyzer:

    def __init__(self, symbol, period="5d", interval="1h"):

        self.symbol = symbol
        self.period = period
        self.interval = interval

    def analyze(self):

        try:

            ticker = yf.Ticker(self.symbol)

            data = ticker.history(
                period=self.period,
                interval=self.interval
            )

            # Safety checks
            if data.empty:
                print(f"{self.symbol}: No data")
                return

            if len(data) < 20:
                print(f"{self.symbol}: Not enough candles")
                return

            # ===== INDICATORS =====

            bb_upper, bb_mid, bb_lower = self.calculate_bb(data)

            ema_signal = self.calculate_ema(data)

            rsi_signal = self.check_rsi_14(data)

            macd_signal = self.calculate_macd(data)

            atr = self.calculate_atr(data)

            current_price = data['Close'].iloc[-1]

            # Skip low volatility chop
            # if atr is None or atr < current_price * 0.003:
            #     print(f"{self.symbol}: Low volatility")
            #     return

            # ===== SIGNAL LOGIC =====

            signal = "Nothing To say at the moment the momentum of the symbol is stable, signals are neutral"

            # BUY setup
            if (
                    current_price <= bb_lower * 1.01
                    and rsi_signal == "BUY"
            ):
                signal = "BUY"

            # SELL setup
            elif (
                    current_price >= bb_upper * 0.99
                    and rsi_signal == "SELL"
            ):
                signal = "SELL"

            current_price = data['Close'].iloc[-1]

            atr = self.calculate_atr(data)

            # ATR FILTER
            if atr is None or atr < current_price * 0.003:
                print(f"{self.symbol}: Low volatility")
                return
            # ===== OUTPUT =====

            if signal:
                return signal

        except Exception as e:

            print(f"\nERROR: {self.symbol}")
            print(e)

            traceback.print_exc()


    def get_price(self):
        ticker = yf.Ticker(self.symbol)

        data = ticker.history(
            period=self.period,
            interval=self.interval
        )

        current_price = data['Close'].iloc[-1]
        return current_price

    # =========================================================
    # INDICATORS
    # =========================================================

    def calculate_bb(self, data):

        sma20 = data['Close'].rolling(20).mean()

        std20 = data['Close'].rolling(20).std()

        upper = sma20 + (2 * std20)

        lower = sma20 - (2 * std20)

        return (
            upper.iloc[-1],
            sma20.iloc[-1],
            lower.iloc[-1]
        )

    def calculate_ema(self, data):

        ema7 = data['Close'].ewm(
            span=7,
            adjust=False
        ).mean()

        ema14 = data['Close'].ewm(
            span=14,
            adjust=False
        ).mean()

        if ema7.iloc[-1] > ema14.iloc[-1]:
            return "UP"

        elif ema7.iloc[-1] < ema14.iloc[-1]:
            return "DOWN"

        return "NEUTRAL"

    def check_rsi_14(self, data):

        delta = data['Close'].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()

        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        latest = rsi.iloc[-1]

        if latest > 70:
            return "SELL"

        elif latest < 30:
            return "BUY"

        return "NEUTRAL"

    def calculate_macd(self, data):

        ema12 = data['Close'].ewm(
            span=12,
            adjust=False
        ).mean()

        ema26 = data['Close'].ewm(
            span=26,
            adjust=False
        ).mean()

        macd = ema12 - ema26

        signal = macd.ewm(
            span=9,
            adjust=False
        ).mean()

        if macd.iloc[-1] > signal.iloc[-1]:
            return "BUY"

        elif macd.iloc[-1] < signal.iloc[-1]:
            return "SELL"

        return "NEUTRAL"

    def calculate_atr(self, data, period=14):

        if len(data) < period:
            return None

        high_low = data['High'] - data['Low']

        high_close = abs(
            data['High'] - data['Close'].shift()
        )

        low_close = abs(
            data['Low'] - data['Close'].shift()
        )

        ranges = pd.concat(
            [high_low, high_close, low_close],
            axis=1
        )

        true_range = ranges.max(axis=1)

        atr = true_range.rolling(period).mean()

        if atr.empty:
            return None

        return atr.iloc[-1]

