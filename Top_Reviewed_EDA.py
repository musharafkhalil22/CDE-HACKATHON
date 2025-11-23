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

def analyze_top_reviewed(df, n=5):
    """Identifies the top N products based on review count."""
    print("\n" + "="*50)
    print(f"## 3. Top {n} Most Reviewed Products ⭐")
    
    # Tabular Analysis: Top N
    top_reviewed = df.sort_values(by='Reviews', ascending=False).head(n)

    print(f"\n--- Top {n} Products by Review Count ---")
    print(top_reviewed[['Category', 'Name', 'Reviews', 'Price', 'Rating']])
    
    # Visualization: Bar Plot of Top N
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Reviews', y='Name', data=top_reviewed, hue='Category', dodge=False)
    plt.title(f'Top {n} Products by Review Count')
    plt.xlabel('Reviews Count')
    plt.ylabel('Product Name')
    plt.show()

if __name__ == "__main__":
    df = load_data(DATA_FILE)
    if df is not None:
        analyze_top_reviewed(df.copy(), n=5)