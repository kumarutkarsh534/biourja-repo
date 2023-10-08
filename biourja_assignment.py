'''
According to me this problem provided all contraints is feasible upto a certain degree of error
processing the data has given the closes output of 12000.48 with only 8% error.

Getting exactly 12000 with 0% error in ratio of zonal wind farms may or may not be possible
as the processing of 100 factorial permutations can take a long time
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from colorama import  init
init()
from prettytable import PrettyTable

csv_file = "input_data.csv"
csv_data = pd.read_csv(csv_file)
des = []
'''
Generate A datastructure with:
1. Id as WindFarm-Name (eg: E1,E2 etc.)
2. Weight forecast/capacity. Fixed for a Farm
3. Capacity
4. Forecast
'''
for row in csv_data.values:
    des.append({"id": row[0], "weight": row[1] / row[2], "forecast": row[1], "capacity": row[2]})

ids = [item['id'] for item in des]
wind_farm_capacities = [item['capacity'] for item in des]
updated_forecast_sums = []
'''
Creating a limit
'''
LIMIT = int(input("Enter the range in which you want to keep it valid. Eg: Enter 500 for +/- 500 from 12000 (recommended 150):  "))
'''
Error in percentage ratio limit 
'''
PER_DIFF_RATIO_LIMIT = int(input("Enter the range in which you want to keep percentage ratio of N,E,W,S. Eg: Enter 5 for 5per error margin (recommended 8per):  "))

'''
Swap the element
'''
def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

'''
Function that ask the user for continuation of the process
'''
def continue_or_not():
    while True:
        b = input("Press Enter to continue or type 'q' to quit: ").strip()
        if not b:
            return True  # User pressed Enter to continue
        elif b.lower() == 'q':
            return False  # User typed 'q' to quit

'''
Function that calculate the sum of each regions for calcualting the ratio of the regions
And calculates the desired target ratio and calculates the difference between them
'''
def calculate_region_statistics(data_objects):
    west_sum_data = 0
    east_sum_data = 0
    south_sum_data = 0
    north_sum_data = 0

    for obj in data_objects:
        first_ch = obj["id"][0]

        if first_ch == 'E':
            east_sum_data += obj["forecast"]
        elif first_ch == 'N':
            north_sum_data += obj["forecast"]
        elif first_ch == 'W':
            west_sum_data += obj["forecast"]
        elif first_ch == 'S':
            south_sum_data += obj["forecast"]

    # Total sum of all regions 
    total = west_sum_data + east_sum_data + south_sum_data + north_sum_data

    west_region_data = (west_sum_data * 100) / total
    east_region_data = (east_sum_data * 100) / total
    south_region_data = (south_sum_data * 100) / total
    north_region_data = (north_sum_data * 100) / total


    # Desired target values
    desired_target_west = 2000
    desired_target_East = 2800
    desired_target_South = 6500
    desired_target_North = 1500
    totalOri = desired_target_East + desired_target_North + desired_target_South + desired_target_west

    # Calculated original ratio percentage
    Orig_west = (desired_target_west * 100) / totalOri
    Orig_east = (desired_target_East * 100) / totalOri
    Orig_south = (desired_target_South * 100) / totalOri
    Orig_north = (desired_target_North * 100) / totalOri

    print(Orig_west)
    print(Orig_east)
    print(Orig_south)
    print(Orig_north)


    # Difference in original ratio percentage and sample ratio percentage
    d_East = Orig_east - east_region_data
    d_West = Orig_west - west_region_data
    d_South = Orig_south - south_region_data
    d_North = Orig_north - north_region_data
    total_PER_DIFF = abs(d_West) + abs(d_East) + abs(d_South) + abs(d_North)
    print("Difference East",d_East)
    print("Difference West",d_West)
    print("Difference South",d_South)
    print("Difference North",d_North)
    print(f"West Region Sum: {west_sum_data} west Original Sum:{Orig_west}")
    print(f"WEST % contribution: {west_region_data}")
    print(f"East Region Sum: {east_sum_data} east Original Sum:{Orig_east}")
    print(f"EAST % contribution: {east_region_data}")
    print(f"North Region Sum: {north_sum_data} north Original Sum:{Orig_north}")
    print(f"NORTH % contribution: {north_region_data}")
    print(f"South Region Sum: {south_sum_data} south Original Sum:{Orig_south}")
    print(f"SOUTH % contribution: {south_region_data}")
    print(f"Total: {total}")

    #checking whether error is minimal
    if(total_PER_DIFF >= PER_DIFF_RATIO_LIMIT*4):
       print("FAILED RATIO MISMATCH")
    else:
        print("SUCCESSFUL!!!!")


'''
Function that generates the permuations of all the input data's
'''
def generate_permutations(arr, start=0):
    if start == len(arr) - 1:
        yield arr.copy() 
    else:
        for i in range(start, len(arr)):
            swap(arr, start, i)
            
            yield from generate_permutations(arr, start + 1)
            
            swap(arr, start, i)

'''
User has to tell that how much limit and error has to be given to satisfied the ouput condition
Validate function which shows the closest permutation and desired output
'''
def validate(ds,cs):
    if(cs >= 12000 - LIMIT and cs <= 12000 + LIMIT):
        table = PrettyTable()
        table.field_names = ds[0].keys()

        # Add ds to the table
        for row in ds:
            table.add_row(row.values())
        print(table)
        print(cs)
        calculate_region_statistics(ds)
        if(not continue_or_not()):
            return False
    return True
for perm in generate_permutations(wind_farm_capacities):
    cur_forecast_sum = 0
    for i in range(len(perm)):
        des[i]["capacity"] = perm[i]
        des[i]["forecast"] = des[i]["weight"]*perm[i] 
        cur_forecast_sum += des[i]["weight"]*perm[i]
    updated_forecast_sums.append(cur_forecast_sum)
    out = validate(des, cur_forecast_sum)
    if(not out):
        plt.plot(updated_forecast_sums)
        plt.show()
        df = pd.DataFrame(des)
        df.to_csv("output_data.csv", index=False)
        break