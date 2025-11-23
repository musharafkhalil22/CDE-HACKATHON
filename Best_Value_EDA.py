import pandas as pd
import numpy as np
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

def analyze_best_value(df):
    """Calculates and ranks products by the 'Reviews per Dollar' metric."""
    print("\n" + "="*50)
    print("## 4. Best Value Metric (Reviews per Dollar) 🏆")
    
    # Create the Value Metric
    df['Value_Metric'] = df['Reviews'] / df['Price']
    df['Value_Metric'].replace([np.inf, -np.inf], 0, inplace=True)

    # Tabular Analysis: Best Value in Each Category
    best_value_per_category = df.loc[df.groupby('Category')['Value_Metric'].idxmax()]
    
    print("\n--- Best Value Product in Each Category (Highest Reviews/Price) ---")
    best_value_display = best_value_per_category[['Category', 'Name', 'Price', 'Reviews', 'Value_Metric']].sort_values(by='Value_Metric', ascending=False)
    print(best_value_display)
    
    # Visualization: Bar Plot of Best Value Products
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Value_Metric', y='Category', data=best_value_display, palette='viridis')
    plt.title('Best Value Metric (Reviews/Price) by Category')
    plt.xlabel('Max Value Metric (Reviews per Dollar)')
    plt.ylabel('Category')
    plt.show()

if __name__ == "__main__":
    df = load_data(DATA_FILE)
    if df is not None:
        analyze_best_value(df.copy())