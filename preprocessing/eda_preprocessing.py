import pandas as pd

pitstop_path = "./Data/f1_pitstops_2018_2024.csv"
df = pd.read_csv(pitstop_path)

df.info()

# Convert 'Date' column to datetime if needed
if df['Date'].dtype == 'object':
    df['Date'] = pd.to_datetime(df['Date'])
    print("'Date' column successfully converted to datetime")

if 'Time_of_race' in df.columns:
    df['Time_of_race'] = df['Time_of_race'].str.replace('Z', '')
    df['Time_of_race'] = pd.to_datetime(df['Time_of_race'], format='%H:%M:%S')

# check for missing values
missing = df.isnull().sum()
print('Missing values in each column:')
print(missing[missing > 0])

# drop rows with any missing values
print("Dropping rows with missing values...")
df_cleaned = df.dropna()
print(f"Number of rows after dropping missing values: {len(df_cleaned)}")
print("Missing values after dropping:")
print(df_cleaned.isnull().sum())

# convert 'Pit_Time' to numeric 
if 'Pit_Time' in df.columns:
    try:
        df['Pit_Time'] = pd.to_numeric(df['Pit_Time'], errors='coerce')
        non_numeric_pit_times = df[df['Pit_Time'].isna()]['Pit_Time'].unique()
        if len(non_numeric_pit_times) > 0:
            print("Non-numeric values found in 'Pit_Time':")
            print(non_numeric_pit_times)
        else:
            print("No non-numeric values found in 'Pit_Time' after conversion.")
    except Exception as e:
        print(f"An error occurred while converting: {e}")

# Export cleaned data
try:
    print("Writing processed data to csv...")
    df_cleaned.to_csv("./Data/cleaned_pitstop_data.csv", index=False)
    print("Successfully exported processed data.")
except Exception as e:
    print(f"Error occurred: {e}")
