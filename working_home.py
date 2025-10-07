import pandas as pd
import calendar
from datetime import datetime
import glob
import sys

# Find Excel files matching pattern
excel_files = glob.glob('transactions-export*.xlsx')

if not excel_files:
    print("No Excel files found matching pattern 'transactions-export*.xlsx'")
    sys.exit(1)
elif len(excel_files) == 1:
    excel_file = excel_files[0]
    print(f"Using file: {excel_file}\n")
else:
    print("Multiple Excel files found:")
    for i, file in enumerate(excel_files, 1):
        print(f"{i}. {file}")
    choice = input("\nSelect file number: ")
    try:
        excel_file = excel_files[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice")
        sys.exit(1)

# Load the Excel file
df = pd.read_excel(excel_file)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Get unique dates when train was taken
train_dates = df['Date'].dt.date.unique()

# Group by year and month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Get all unique year-month combinations
year_months = df[['Year', 'Month']].drop_duplicates().sort_values(['Year', 'Month'])

def print_calendar(year, month, highlight_dates):
    """Print a calendar with highlighted dates"""
    # Get the month name and year
    month_name = calendar.month_name[month]
    print(f"\n{month_name} {year}".center(28))

    # Print weekday headers
    print("ma  di  wo  do  vr  za  zo")

    # Get calendar matrix for the month
    cal = calendar.monthcalendar(year, month)

    # Print each week
    for week in cal:
        week_str = []
        for day in week:
            if day == 0:
                week_str.append("    ")  # Empty cell
            else:
                day_date = datetime(year, month, day).date()
                if day_date in highlight_dates:
                    # Highlight with underline using ANSI codes
                    week_str.append(f"\033[4m{day:2d}\033[0m  ")
                else:
                    week_str.append(f"{day:2d}  ")
        print("".join(week_str))

# Print calendar for each month
highlight_set = set(train_dates)

for _, row in year_months.iterrows():
    print_calendar(int(row['Year']), int(row['Month']), highlight_set)

print(f"\n\nTotal days with train travel: {len(train_dates)}")
print(f"Total journeys: {len(df)}")
