"# Banggood Data Pipeline Project" 
I have completed the full Banggood Product Data Pipeline project as required in the Case Study Exam. The project includes end-to-end implementation of web scraping, data transformation, exploratory data analysis, SQL loading, and aggregated SQL analytics.

Part 1 — Data Extraction (Web Scraping)

Scraped 5 selected categories from Banggood.com using requests, BeautifulSoup, and Selenium.

Extracted product name, price, rating, review count, product URL, and stock availability.

Implemented multi-page pagination and stored the scraped output in CSV format.

Part 2 — Data Cleaning & Transformation

Loaded raw data into pandas and cleaned price, rating, and review fields.

Handled missing values and standardized formats.

Created derived features such as Value Score (rating/price) and Review Intensity (reviews per price unit).

Part 3 — Exploratory Data Analysis (Minimum 5 Analyses)

Performed multiple category-wise and overall analyses using Python, including:

Price distribution

Rating vs price correlation

Top reviewed products

Best value products

Stock availability percentage

All analyses include visualizations and insights.

Part 4 — Load into SQL Server

Created SQL schema for storing product data.

Loaded cleaned data into SQL Server using pyodbc.

Validated inserts through row-count checks and sample queries.

Part 5 — SQL Aggregated Analysis (Minimum 5 Queries)

Wrote and executed SQL queries including:

Average price per category

Average rating per category

Product count per category

Top 5 reviewed items

Stock availability percentage
