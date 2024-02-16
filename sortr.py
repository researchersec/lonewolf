import json
from datetime import datetime, timedelta
import os

# Function to calculate historic data based on the provided interval
def calculate_historic_data(latest_data, files, days_interval):
    historic_data = {}

    # Determine the end date as the current date
    end_date = datetime.now()

    # Calculate the start date based on the days_interval
    start_date = end_date - timedelta(days=days_interval)

    # Iterate over each filename
    for filename in files:
        # Parse the timestamp from the filename
        timestamp_date = parse_timestamp(filename)

        # Check if the timestamp falls within the specified interval
        if start_date <= timestamp_date <= end_date:
            # Read data from the file and update historic_data
            with open(os.path.join('prices', filename), 'r') as file:
                data = json.load(file)
                historic_data.update(data)

    return historic_data

# Function to parse timestamp from filename and convert to datetime object
def parse_timestamp(filename):
    # Extract timestamp from filename
    timestamp_str = os.path.splitext(filename)[0]

    # Split the timestamp string using '_' as the delimiter
    date_str, time_str = timestamp_str.split('_')

    # Extract date components
    year, month, day = map(int, date_str.split('-'))

    # Extract time components
    hour, minute, second = map(int, time_str.split('-'))

    # Create datetime object
    return datetime(year, month, day, hour, minute, second)

# Get list of filenames in the 'lonewolf/prices' directory
files_in_prices_dir = os.listdir('prices')

# Filter files with the specified timestamp format
filtered_files = [filename for filename in files_in_prices_dir if filename.endswith('.json') and len(filename) == 24 and filename[4] == '-' and filename[7] == '-' and filename[10] == '_' and filename[13] == '-' and filename[16] == '-']

print("Filtered files:", filtered_files)

# Sort filenames by timestamp (oldest to newest)
sorted_files = sorted(filtered_files, key=parse_timestamp)

print("Sorted files:", sorted_files)

# Check if any files matching the specified timestamp format were found
if sorted_files:
    # Read latest pricing data from the 'latest.json' file
    with open(os.path.join('prices', 'latest.json'), 'r') as file:
        latest_data = json.load(file)

    # Calculate historic data (e.g., for the last day, last week, last month)
    day_data = calculate_historic_data(latest_data, sorted_files, 1)
    week_data = calculate_historic_data(latest_data, sorted_files, 7)
    month_data = calculate_historic_data(latest_data, sorted_files, 30)

    if day_data:
        print("Day data:", day_data)
    else:
        print("No data found for day.")
    if week_data:
        print("Week data:", week_data)
    else:
        print("No data found for week.")
    if month_data:
        print("Month data:", month_data)
    else:
        print("No data found for month.")
    
    # Write historic data to separate files
    if day_data:
        with open(os.path.join('prices', 'day.json'), 'w') as file:
            json.dump(day_data, file, indent=4)
    if week_data:
        with open(os.path.join('prices', 'week.json'), 'w') as file:
            json.dump(week_data, file, indent=4)
    if month_data:
        with open(os.path.join('prices', 'month.json'), 'w') as file:
            json.dump(month_data, file, indent=4)
else:
    print("No files found matching the specified timestamp format.")
