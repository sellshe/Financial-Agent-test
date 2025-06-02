from crewai import Agent, Task, Crew
import yfinance as yf
import pandas as pd

# ========== Agent Definitions ==========

screener = Agent(
    name="StockScreenerAgent",
    role="Stock Screener",
    goal="Find 3 fundamentally strong US stocks for long-term investment",
    backstory="Experienced in identifying undervalued US equities based on fundamentals"
)

buyer = Agent(
    name="BuyAdvisorAgent",
    role="Buy Advisor",
    goal="Suggest how much to invest in each selected stock given a $5000 budget",
    backstory="Expert in portfolio allocation and risk-adjusted investment planning"
)

seller = Agent(
    name="SellAdvisorAgent",
    role="Sell Advisor",
    goal="Suggest when to sell stocks if they underperform or reach 20% gain",
    backstory="Skilled in long-term performance monitoring and sell decision-making"
)

# ========== Stock Screener Logic ==========
def screen_stocks():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'JNJ', 'V', 'MA', 'UNH', 'HD', 'PG']
    selected = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            pe = info.get('trailingPE')
            peg = info.get('pegRatio')
            if pe and peg and pe < 25 and peg < 2:
                selected.append((ticker, pe, peg))
        except:
            continue
    return sorted(selected, key=lambda x: (x[1], x[2]))[:3]

# ========== Tasks ==========
screen_task = Task(
    agent=screener,
    description="Screen 10 popular US stocks for low P/E and PEG values to select top 3."
)

buy_task = Task(
    agent=buyer,
    description="Allocate $5000 evenly across the 3 selected stocks and suggest how many shares to buy."
)

sell_task = Task(
    agent=seller,
    description="Advise when to sell stocks: sell if price increases >20% or drops >15%."
)

# ========== Crew and Execution ==========
crew = Crew(
    name="LongTermInvestmentCrew",
    tasks=[screen_task, buy_task, sell_task]
)

# Run screening and basic logic manually here
screened = screen_stocks()
print("\nTop 3 screened stocks:")
for s in screened:
    print(f"{s[0]} | P/E: {s[1]} | PEG: {s[2]}")

# Simple Buy Allocation
budget = 5000
per_stock = budget / len(screened)
print("\nBuy Recommendations:")
for ticker, _, _ in screened:
    price = yf.Ticker(ticker).history(period="1d")['Close'][-1]
    shares = int(per_stock / price)
    print(f"Buy {shares} shares of {ticker} at ${price:.2f} per share")
