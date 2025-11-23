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

def analyze_rating_vs_price(df):
    """Calculates correlation and visualizes the relationship between rating and price."""
    print("\n" + "="*50)
    print("## 2. Rating vs. Price Correlation 📈")

    # Tabular Analysis: Overall Correlation
    correlation = df['Rating'].corr(df['Price'])
    print(f"\nOverall Pearson Correlation (Rating vs. Price): {correlation:.3f}")

    # Analysis by Price Segment
    segment_correlation = df.groupby('Price_Segment')['Price', 'Rating'].corr().unstack().iloc[:, 1]
    print("\nCorrelation by Price Segment:")
    print(segment_correlation)

    # Visualization: Scatter Plot
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x='Price', y='Rating', hue='Category', data=df)
    plt.title(f'Rating vs. Price (Correlation: {correlation:.3f})')
    plt.xlabel('Price (USD)')
    plt.ylabel('Rating')
    plt.show()

if __name__ == "__main__":
    df = load_data(DATA_FILE)
    if df is not None:
        analyze_rating_vs_price(df.copy())