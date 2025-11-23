import pandas as pd
import numpy as np

# --- 1. Load Scraped Data ---
def load_data(file_path="banggood_5_categories.csv"):
    """Loads the data and prints initial info."""
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Data loaded successfully. Shape: {df.shape}")
        print("\n--- Initial Missing Values ---")
        print(df.isnull().sum())
        return df
    except FileNotFoundError:
        print(f"❌ Error: File not found at {file_path}. Ensure the scraping script ran.")
        return pd.DataFrame()

# --- 2. Clean Data (Price, Rating, Reviews, Missing Values) ---
def clean_data(df):
    """Cleans and standardizes the columns."""
    if df.empty:
        return df

    print("\n--- Starting Data Cleaning ---")

    # A. Clean 'Price' Column
    # The price is expected to be a string like '$19.99' or '£10.50'.
    def clean_price(price):
        if pd.isna(price) or price == 'N/A':
            return np.nan
        # Remove all non-digit characters except the decimal point
        cleaned = ''.join(c for c in str(price) if c.isdigit() or c == '.')
        try:
            return float(cleaned)
        except ValueError:
            return np.nan # Return NaN if conversion fails

    df['Price'] = df['Price'].apply(clean_price)
    print(f"    - Price cleaned: Converted to numeric (float). Missing values: {df['Price'].isnull().sum()}")

    # B. Clean 'Rating' and 'Reviews' (Since these were placeholders in the scrape script)
    # Convert 'Rating' to float and fill 'N/A' (or any non-numeric) with 0.0
    # For a real scrape, you'd apply a cleaning function similar to price.
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').fillna(0.0)
    # Ensure 'Reviews' is an integer, treating '0' and 'N/A' placeholders as 0
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0).astype(int)
    
    # C. Handle Missing Values
    # Drop rows where 'Name' or 'Price' are missing, as these are critical.
    df.dropna(subset=['Name', 'Price'], inplace=True)
    
    # Fill remaining 'URL' N/A values with a placeholder
    df['URL'].fillna('NO_URL_FOUND', inplace=True)

    print(f"    - Cleaned shape after dropping critical NaNs: {df.shape}")
    print("    - Rating and Reviews standardized (filled NaNs with 0).")
    return df

# --- 3. Create Additional Derived Features ---
def feature_engineering(df):
    """Creates new, insightful features."""
    if df.empty:
        return df

    print("\n--- Creating Derived Features ---")
    
    # FEATURE 1: Price Segment (Categorical feature based on price)
    # Rationale: The original bins failed if df['Price'].max() <= 200.
    
    bins = [0, 10, 50, 200]
    labels = ['Budget (<$10)', 'Mid-Range ($10-50)', 'Premium ($50-200)', 'High-End (>$200)']
    
    # 💡 FIX: Ensure the final bin edge is strictly greater than the preceding one (200).
    max_price_plus_one = df['Price'].max() + 1
    
    # If the max price is 150, last_bin becomes max(201, 151) = 201.
    # If the max price is 500, last_bin becomes max(201, 501) = 501.
    # This prevents the non-monotonic error.
    last_bin = max(201, max_price_plus_one) 
    
    bins.append(last_bin) # Add the safe last bin

    df['Price_Segment'] = pd.cut(df['Price'], bins=bins, labels=labels, right=False, include_lowest=True)
    print("    - Feature 'Price_Segment' created.")

    # FEATURE 2: Product Name Length (Numeric feature)
    df['Name_Length'] = df['Name'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)
    print("    - Feature 'Name_Length' created.")
    
    # FEATURE 3: Price per Character (Example of a ratio feature)
    df['Price_Per_Char'] = df.apply(
        lambda row: row['Price'] / row['Name_Length'] if row['Name_Length'] > 0 else 0, 
        axis=1
    )
    print("    - Feature 'Price_Per_Char' created.")

    return df

# --- Main Execution ---
if __name__ == "__main__":
    
    # 1. Load Data
    df_raw = load_data()

    if not df_raw.empty:
        # 2. Clean Data
        df_cleaned = clean_data(df_raw.copy())

        # 3. Create Features
        df_final = feature_engineering(df_cleaned.copy())

        # --- Final Summary ---
        print("\n--- FINAL DATASET SUMMARY ---")
        print(f"Final Cleaned Shape: {df_final.shape}")
        print("\nColumn Data Types:")
        print(df_final.dtypes)
        print("\nExample Data:")
        print(df_final[['Category', 'Name', 'Price', 'Price_Segment', 'Name_Length', 'Price_Per_Char']].head())
        
        # Save the final transformed data
        df_final.to_csv("banggood_transformed_data.csv", index=False)
        print("\n✅ Transformed data saved to 'banggood_transformed_data.csv'")