import os
import pandas as pd 
import importlib
from io import StringIO
import datetime as dt
import numpy as np

# Load column headers from a separate header file
def initialize_columns(path, line):
    path = 'data/' + path
    with open(path, "r") as file:
        lines = file.readlines()
        return lines[1].lower()  # return header line

# Clean and preprocess a single race file
def clean(path, date, header_path=None, header_line=None):
    CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    os.chdir(CURRENT_DIRECTORY)

    path = 'data/' + path
    with open(path, "r") as file:
        lines = file.readlines()
        cleaned_data = []

        # Use external header file if provided
        if header_path is not None:
            cleaned_data.append(initialize_columns(header_path, header_line))
        else:
            cleaned_data.append(lines[1].lower())

        for line in lines:
            line = line.strip()
            if line == "":
                continue  # skip blank lines

            # Skip known header-like lines that appear mid-file
            headers = [
                'place', 'beginner', '3-5th', '1-2nd', 'cat', 'clydesdale',
                'high', 'male', 'female', 'middle', 'nonbinary', 'single', 'tandem', 'unicycle'
            ]
            if line.lower().startswith(tuple(headers)):
                continue

            cleaned_data.append(line)  # valid data row

    # Read cleaned rows into DataFrame
    cleaned_str = "\n".join(cleaned_data)
    df = pd.read_csv(StringIO(cleaned_str), sep='\t')
    df = df.iloc[1:]  # skip repeated header row

    # Rename unnamed columns to 'lap N'
    counter = 0
    new_columns = []
    for column in df.columns:
        if column.startswith('lap '):
            counter = int(column[-1])
        if column.startswith("Unnamed: "):
            counter += 1
            column = f'lap {counter}'
        new_columns.append(column)
    df.columns = new_columns

    # Add race date
    df['date'] = pd.Timestamp(date)

    # Convert lap times to seconds (handle NaNs and dashes)
    df.replace('-', np.nan, inplace=True)
    for column in new_columns:
        if column.startswith('lap '):
            mask = df[column].notna()
            df.loc[mask, column] = pd.to_timedelta('00:' + df.loc[mask, column], errors='coerce').dt.total_seconds()
            df[column] = pd.to_numeric(df[column], errors='coerce')

    # Compute average lap time excluding Lap 1 (too variable)
    lap_columns = df.filter(regex=r'lap (?!.*1)').columns
    df['average_lap_time'] = df[lap_columns].mean(axis=1)

    return df

# Load and combine multiple race files into one DataFrame
def join_all(file_list, date_list, header_path=None, header_line=None):
    print(f"Initializing main data frame based on: {file_list[0]}")
    main_df = clean(file_list[0], date_list[0], header_path, header_line)
    for i in range(len(file_list)):
        print(f"Appending: {file_list[i]}")
        main_df = pd.concat([main_df, clean(file_list[i], date_list[i])])
    return main_df

# Race files and corresponding dates
events = [
    'Barnburner at Steilacoom 2023.txt', 'Starcrossed at Marymoor 2023.txt', 'Beach Party At Silver Lake 2023.txt',
    'Magnuson Park Cross 2023.txt', 'North 40 at LeMay 2023.txt', 'Woodland Park GP 2023.txt',
    'The Beach Party at Silver Lake 2024.txt', 'Starcrossed at Marymoor 2024.txt', 'Barnburner at Steilacoom 2024.txt',
    'Magnuson Park Cross 2024.txt', 'North 40 - LeMay 2024.txt', 'Woodland Park Gran Prix 2024.txt'
]
dates = [
    'Sep 10, 2023', 'Sep 23, 2023', 'Oct 8, 2023', 'Oct 22, 2023', 'Nov 5, 2023', 'Nov 19, 2023',
    'Sep 8, 2024', 'Sep 21, 2024', 'Oct 6, 2024', 'Oct 20, 2024', 'Nov 3, 2024', 'Nov 17, 2024'
]

# Assemble complete dataset
df = join_all(events, dates, events[-1], 331)

# Preview columns
df.columns