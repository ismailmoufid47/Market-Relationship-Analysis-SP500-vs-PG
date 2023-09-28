import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Default start and end dates
default_start_date = "2000-01-01"
default_end_date = "2023-01-01"

# Function to validate a date in YYYY-MM-DD format
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to check if a date is not in the future or present
def is_not_future_date(date_str, include_present):
    today = datetime.now().date()
    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    if include_present == True:
        return selected_date <= today
    else:
        return selected_date < today



# Prompt the user for the start date (or press Enter to use the default)
start_date = input(f"Enter the start date (YYYY-MM-DD, or press Enter for default value: {default_start_date}): ")

# Use the default start date if the user presses Enter
if start_date == "":
    start_date = default_start_date

# Validate the start date format and future date
while not is_valid_date(start_date) or not is_not_future_date(start_date, False):
    print("Invalid date format or future/present date. Please try again.")
    start_date = input("Enter the start date (YYYY-MM-DD): ")

# Prompt the user for the end date (or press Enter to use the default)
end_date = input(f"Enter the end date (YYYY-MM-DD, or press Enter for default value: {default_end_date}): ")

# Use the default end date if the user presses Enter
if end_date == "":
    end_date = default_end_date

# Validate the end date format and future date
while not is_valid_date(end_date) or not is_not_future_date(end_date, True):
    print("Invalid date format or future date. Please try again.")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

# Define the ticker symbols
sp500_ticker = '^GSPC'  # S&P 500
pg_ticker = 'PG'  # Procter & Gamble

# Download historical data
sp500_data = yf.download(sp500_ticker, start= start_date, end= end_date)
pg_data = yf.download(pg_ticker, start=start_date, end=end_date)

# Handle missing data by forward filling (replace missing values with the previous day's value)
sp500_data.ffill()
pg_data.ffill()

# Calculate daily returns for both S&P 500 and PG
sp500_data['Daily_Return'] = sp500_data['Adj Close'].pct_change()
pg_data['Daily_Return'] = pg_data['Adj Close'].pct_change()

# Calculate mean (average) daily returns
mean_sp500_return = sp500_data['Daily_Return'].mean()
mean_pg_return = pg_data['Daily_Return'].mean()

# Calculate standard deviation of daily returns
std_sp500_return = sp500_data['Daily_Return'].std()
std_pg_return = pg_data['Daily_Return'].std()

print("S&P 500 Mean Daily Return:", mean_sp500_return)
print("Procter & Gamble (PG) Mean Daily Return:", mean_pg_return)

print("\nS&P 500 Standard Deviation of Daily Returns:", std_sp500_return)
print("Procter & Gamble (PG) Standard Deviation of Daily Returns:", std_pg_return)

sp500_returns = sp500_data['Daily_Return'].dropna()  # Drop any potential NaN values
pg_returns = pg_data['Daily_Return'].dropna()  # Drop any potential NaN values

# Compute the correlation coefficient
correlation_coefficient = np.corrcoef(sp500_returns, pg_returns)[0, 1]

print("Correlation Coefficient between S&P 500 and Procter & Gamble (PG):", correlation_coefficient)

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot scatter plot of daily returns
ax1.scatter(sp500_data['Daily_Return'], pg_data['Daily_Return'], alpha=0.5)
ax1.set_title('Scatter Plot of Daily Returns')
ax1.set_xlabel('S&P 500 Daily Return')
ax1.set_ylabel('Procter & Gamble (PG) Daily Return')
ax1.grid(True)

# Normalize prices to a common starting point ($100)
sp500_normalized = sp500_data['Adj Close'] / sp500_data['Adj Close'].iloc[0] * 100
pg_normalized = pg_data['Adj Close'] / pg_data['Adj Close'].iloc[0] * 100

# Plot normalized prices
ax2.plot(sp500_data.index, sp500_normalized, label='S&P 500', color='blue')
ax2.plot(pg_data.index, pg_normalized, label='Procter & Gamble (PG)', color='green')
ax2.set_title('Normalized Prices of S&P 500 and Procter & Gamble (PG)')
ax2.set_xlabel('Date')
ax2.set_ylabel('Normalized Price (Starting at $100)')
ax2.legend()
ax2.grid(True)

# Adjust layout and show both plots
plt.tight_layout()
plt.show()