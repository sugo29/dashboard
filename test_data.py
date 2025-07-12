import pandas as pd

# Test the data loading
df = pd.read_excel('dummy_data.xlsx', header=0)
print("Initial shape:", df.shape)
print("First cell:", df.iloc[0, 0])

if df.iloc[0, 0] == 'MONTH':
    # Use the first row as column names and drop it
    df.columns = df.iloc[0]
    df = df.drop(df.index[0]).reset_index(drop=True)

print("After fixing - Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Unique stores:", df['STORE'].nunique())
print("Sample data:")
print(df.head())
