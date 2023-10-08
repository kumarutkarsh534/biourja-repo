# Import necessary libraries and modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from colorama import init  # Initialize colorama module
init()  # Initialize colorama
from prettytable import PrettyTable

# Load data from a CSV file
csv_file = "input_data.csv"
csv_data = pd.read_csv(csv_file)
des = []  # Create a list to store data objects

# Create a data structure for each wind farm with id, weight, capacity, and forecast
for row in csv_data.values:
    des.append({"id": row[0], "weight": row[1] / row[2], "forecast": row[1], "capacity": row[2]})

ids = [item['id'] for item in des]
wind_farm_capacities = [item['capacity'] for item in des]
updated_forecast_sums = []  # List to store updated forecast sums

# Define a limit for valid output
LIMIT = int(input("Enter the range within which you want the output to be valid (e.g., Enter 500 for +/- 500 from 12000, recommended 150):  "))

# Define a percentage difference ratio limit
PER_DIFF_RATIO_LIMIT = int(input("Enter the range within which you want to keep the percentage ratio of N, E, W, S (e.g., Enter 5 for a 5% error margin, recommended 8%):  "))

# Define a function to swap elements in an array
def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

# Define a function to ask the user for continuation of the process
def continue_or_not():
    while True:
        b = input("Press Enter to continue or type 'q' to quit: ").strip()
        if not b:
            return True  # User pressed Enter to continue
        elif b.lower() == 'q':
            return False  # User typed 'q' to quit

# Define a function to calculate the sum of each region and the difference from the desired target ratio
def calculate_region_statistics(data_objects):
    # Initialize sums for each region
    west_sum_data = 0
    east_sum_data = 0
    south_sum_data = 0
    north_sum_data = 0

    # Calculate sums for each region
    for obj in data_objects:
        first_ch = obj["id"][0]
        if first_ch == 'E':
           
