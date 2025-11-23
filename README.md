📊 Banggood Data Pipeline Project

This project delivers a complete end-to-end data engineering and analytics pipeline, fulfilling all requirements of the Banggood Case Study Exam. It covers web scraping, data cleaning, exploratory analysis, SQL Server loading, and SQL aggregated reporting.

🧩 Part 1 — Data Extraction (Web Scraping)

✔ Scraped 5 Banggood categories using:

requests

BeautifulSoup

Selenium

✔ Extracted:

Product Name

Price

Rating

Review Count

Product URL

Stock Availability

✔ Implemented:

Full pagination

Error handling

Export to CSV

🧹 Part 2 — Data Cleaning & Transformation

✔ Loaded raw CSV into pandas
✔ Cleaned price, rating, and review values
✔ Handled missing and inconsistent data
✔ Standardized formats across all categories

🔧 Derived Features

Value Score = rating ÷ price

Review Intensity = reviews per price unit

📈 Part 3 — Exploratory Data Analysis (EDA)

Performed 5+ visual analyses, including:

📌 Price Distribution per Category

📌 Rating vs Price Correlation

📌 Top Reviewed Products

📌 Best Value Products

📌 Stock Availability Percentage

All insights generated through Python visualizations and statistical summaries.

🗄 Part 4 — Load Data into SQL Server

✔ Designed SQL schema (single or multi-table)
✔ Inserted transformed data using pyodbc
✔ Validated load using row-count and sample queries

🧮 Part 5 — SQL Aggregated Analysis

Executed 5+ analytical SQL queries, including:

Average price per category

Average rating per category

Product count per category

Top 5 reviewed items

Stock availability percentage
