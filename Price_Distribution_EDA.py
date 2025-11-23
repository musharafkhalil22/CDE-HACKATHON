import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = "banggood_transformed_data.csv"
sns.set_style("whitegrid")

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found.")
        return None

def analyze_price_distribution(df):
    """Calculates and visualizes the statistical summary of prices by category."""
    print("\n" + "="*50)
    print("## 1. Price Distribution per Category 💰")
    
    price_summary = df.groupby('Category')['Price'].agg(
        ['count', 'mean', 'median', 'std', 'min', 'max']
    ).sort_values(by='mean', ascending=False)
    
    print("\n--- Summary Statistics (Price per Category) ---")
    print(price_summary)

    # Visualization: Box Plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Category', y='Price', data=df)
    plt.title('Price Distribution by Category (Box Plot)')
    plt.xlabel('Category')
    plt.ylabel('Price (USD)')
    plt.ylim(0, df['Price'].quantile(0.95))
    plt.show()

if __name__ == "__main__":
    df = load_data(DATA_FILE)
    if df is not None:
        analyze_price_distribution(df.copy())