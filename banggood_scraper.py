import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os

# --- STEP 0: Log Function ---
def log_progress(message):
    timestamp_format = '%Y-%m-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    print(f"{timestamp} : {message}")
    try:
        with open('code_log.txt', 'a', encoding='utf-8') as f:
            f.write(timestamp + ' : ' + message + '\n')
    except:
        pass

# --- STEP 1: Extract Function ---
def extract(url, category_name):
    log_progress(f"Starting extraction for Category: {category_name}")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        log_progress(f"URL Opened: {url}")
        
        # Scrolling
        log_progress("Scrolling to load products...")
        for i in range(1, 6):
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {i/6});")
            time.sleep(2)
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        data = []
        
        # Finding Cards
        cards = soup.select(".product-item")
        if not cards:
            cards = soup.select(".p-wrap") # Fallback
            
        log_progress(f"Found {len(cards)} cards in {category_name}.")

        for c in cards:
            try:
                # Name
                link_tag = c.select_one("a")
                name = link_tag.get("title") if link_tag else None
                if not name: 
                    img_tag = c.select_one("img")
                    name = img_tag.get("alt") if img_tag else None

                # Price
                price_tag = c.select_one(".price")
                if not price_tag: price_tag = c.select_one(".price-box")
                price = price_tag.get_text(strip=True) if price_tag else "N/A"
                
                # URL
                product_url = link_tag["href"] if link_tag else "N/A"
                if product_url != "N/A" and not product_url.startswith("http"):
                    product_url = "https://www.banggood.com" + product_url

                # Add Data if Name exists
                if name:
                    data.append({
                        "Category": category_name,  # <--- Naya Column
                        "Name": name,
                        "Price": price,
                        "Rating": "N/A", # Placeholder
                        "Reviews": "0",  # Placeholder
                        "URL": product_url
                    })
            except:
                continue

        df = pd.DataFrame(data)
        log_progress(f"Finished {category_name}. Extracted: {len(df)} rows")
        return df
        
    except Exception as e:
        log_progress(f"Error in {category_name}: {e}")
        return pd.DataFrame()
    finally:
        driver.quit()

# --- MAIN EXECUTION BLOCK (Loop for 5 Categories) ---
if __name__ == "__main__":
    
    # 5 Categories ki List (Dictionary)
    categories = {
        "Sports": "https://www.banggood.com/Wholesale-Sports-and-Outdoors-ca-6001.html",
        "Electronics": "https://www.banggood.com/Wholesale-Consumer-Electronics-ca-4001.html",
        "Tools": "https://www.banggood.com/Wholesale-Tools-ca-3001.html",
        "Toys": "https://www.banggood.com/Wholesale-Toys-Hobbies-and-Robot-ca-7001.html",
        "Automobiles": "https://www.banggood.com/Wholesale-Automobiles-and-Motorcycles-ca-8001.html"
    }

    all_data_frames = [] # Yahan sab jama karenge

    print("--- BATCH EXTRACTION STARTED ---")

    # Loop chalao har category ke liye
    for cat_name, cat_url in categories.items():
        print(f"\nProcessing: {cat_name}...")
        df_temp = extract(cat_url, cat_name)
        
        if not df_temp.empty:
            all_data_frames.append(df_temp)
        else:
            print(f"Skipping {cat_name} due to error.")

    # Sab ko Join (Concat) karo
    if all_data_frames:
        final_df = pd.concat(all_data_frames, ignore_index=True)
        
        print("\n--- FINAL SUCCESS ---")
        print(f"Total Products Scraped: {len(final_df)}")
        print(final_df['Category'].value_counts()) # Har category me kitne items aye
        
        # Final Save
        final_df.to_csv("banggood_5_categories.csv", index=False)
        print("Data saved to 'banggood_5_categories.csv'")
    else:
        print("No data extracted from any category.")