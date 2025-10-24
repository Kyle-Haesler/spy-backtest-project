import pandas as pd



def load_spy_data (csv_file = "../data/spy_daily.csv"):
    """
    Loads SPY daily data from CSV into a cleaned pandas DataFrame
    
    Args:
        csv_file(str): Path to the CSV file
    
    Returns:
        pd.DataFrame: DataFrame with Date as index and sorted chronologically
    """
    data = pd.read_csv(csv_file, parse_dates=["Date"])
    data.set_index("Date", inplace=True)
    data.sort_index(inplace=True)
    return data

if __name__ == "__main__":
    df = load_spy_data()
    print(df.head())