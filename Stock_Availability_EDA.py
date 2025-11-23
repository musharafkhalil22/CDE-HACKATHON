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

def analyze_stock_proxy(df):
    """Analyzes the average name length across price segments as a proxy for inventory detail."""
    print("\n" + "="*50)
    print("## 5. Product Detail Analysis (Name Length Proxy) 🏷️")
    
    # Tabular Analysis: Average Name Length by Category
    name_length_summary = df.groupby('Category')['Name_Length'].agg(
        ['mean', 'median', 'std', 'count']
    ).sort_values(by='mean', ascending=False)
    
    print("\n--- Average Product Name Length by Category ---")
    print(name_length_summary)
    
    # Tabular Analysis: Name Length by Price Segment
    name_length_segment = df.groupby('Price_Segment')['Name_Length'].mean()
    print("\nAverage Name Length by Price Segment:")
    print(name_length_segment)
    
    # Visualization: Bar Plot
    plt.figure(figsize=(8, 5))
    sns.barplot(x=name_length_segment.index, y=name_length_segment.values, palette='magma')
    plt.title('Average Name Length by Price Segment')
    plt.xlabel('Price Segment')
    plt.ylabel('Average Product Name Length')
    plt.xticks(rotation=45, ha='right')
    plt.show()

if __name__ == "__main__":
    df = load_data(DATA_FILE)
    if df is not None:
        analyze_stock_proxy(df.copy())