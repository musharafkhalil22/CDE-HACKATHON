import pandas as pd
import numpy as np
import pyodbc
from time import sleep

# --- 1. Configuration (UPDATED with your server details) ---
SQL_CONFIG = {
    'DRIVER': '{ODBC Driver 17 for SQL Server}',
    # CRITICAL FIX: Your identified Server Name
    'SERVER': 'INTELPROGRAMER', 
    
    # Your identified Database Name
    'DATABASE': 'Banggood_Final', 
    
    # Final Connection String using Windows Authentication
    'CONNECTION_STRING': 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=INTELPROGRAMER;DATABASE=Banggood_Final;Trusted_Connection=yes;'
}

DATA_FILE = "banggood_transformed_data.csv"
TABLE_NAME = "BanggoodProducts"

# --- 2. Database Connection ---
def get_connection():
    """Establishes and returns a pyodbc connection object."""
    # The SERVER and DATABASE are now hardcoded in the CONNECTION_STRING above, 
    # so we use that directly.
    conn_str = SQL_CONFIG['CONNECTION_STRING']
    try:
        conn = pyodbc.connect(conn_str)
        print("✅ Successfully connected to SQL Server.")
        return conn
    except pyodbc.Error as ex:
        # We check the first part of the error message for better diagnosis
        sqlstate = ex.args[0]
        print(f"❌ Connection Error: {sqlstate}")
        print("Please verify the SQL Server service is running and the name 'INTELPROGRAMER' is correct.")
        return None

# --- 3. Database Schema (Table Creation) ---
def create_table_schema(cursor):
    """Creates the unified table schema, matching the DataFrame columns and types."""
    
    create_table_sql = f"""
    -- Drop the table if it exists to allow fresh runs
    IF OBJECT_ID('{TABLE_NAME}', 'U') IS NOT NULL 
        DROP TABLE {TABLE_NAME};
        
    CREATE TABLE {TABLE_NAME} (
        ProductID INT PRIMARY KEY IDENTITY(1,1),
        Category NVARCHAR(50),
        Name NVARCHAR(500) NOT NULL,
        Price DECIMAL(10, 2),
        Rating DECIMAL(3, 2),
        Reviews INT,
        URL NVARCHAR(1000),
        Price_Segment NVARCHAR(50),
        Name_Length INT,
        Price_Per_Char DECIMAL(10, 4)
    );
    """
    try:
        cursor.execute(create_table_sql)
        cursor.connection.commit()
        print(f"✅ Table '{TABLE_NAME}' created successfully in {SQL_CONFIG['DATABASE']}.")
    except pyodbc.Error as ex:
        print(f"❌ Error creating table: {ex}")

# --- 4. Data Insertion ---
def insert_data(cursor, df):
    """Inserts DataFrame rows into the SQL table using executemany."""
    
    # Column names must match the DataFrame and the SQL table structure exactly
    cols = ['Category', 'Name', 'Price', 'Rating', 'Reviews', 'URL', 'Price_Segment', 'Name_Length', 'Price_Per_Char']
    placeholders = ', '.join(['?'] * len(cols))
    insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(cols)}) VALUES ({placeholders})"

    # Prepare data: pyodbc requires None for SQL NULLs, so we convert NumPy NaNs
    data_to_insert = df[cols].replace({np.nan: None}).values.tolist()

    print(f"⏳ Starting insertion of {len(data_to_insert)} rows...")
    
    try:
        # Use executemany for fast, batch insertion
        cursor.executemany(insert_sql, data_to_insert)
        cursor.connection.commit()
        print(f"✅ Data successfully inserted into {TABLE_NAME}.")
        return True
    except pyodbc.Error as ex:
        print(f"❌ Error during data insertion: {ex}")
        cursor.connection.rollback()
        return False

# --- 5. Validation ---
def validate_insertion(cursor, expected_count):
    """Queries the database to confirm the number of inserted rows."""
    
    count_sql = f"SELECT COUNT(*) FROM {TABLE_NAME}"
    cursor.execute(count_sql)
    actual_count = cursor.fetchone()[0]
    
    print("\n--- Validation ---")
    print(f"Expected rows (from CSV): {expected_count}")
    print(f"Actual rows (in SQL Server): {actual_count}")
    
    if actual_count == expected_count:
        print("✅ Validation successful: Row counts match.")
    else:
        print("⚠️ Validation mismatch: Row counts do not match!")
    
    return actual_count

# --- Main Execution ---
def main():
    # Load the cleaned data
    try:
        df = pd.read_csv(DATA_FILE)
        # Drop rows where 'Category' or 'Name' is null just in case
        df.dropna(subset=['Category', 'Name'], inplace=True)
        expected_rows = len(df)
        print(f"Loaded {expected_rows} rows from CSV for insertion.")
    except FileNotFoundError:
        print(f"❌ Data file '{DATA_FILE}' not found. Cannot proceed.")
        return

    # 1. Connect to SQL Server
    conn = get_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        
        # 2. Create Schema
        create_table_schema(cursor)
        
        # 3. Insert Data
        if insert_data(cursor, df):
            # 4. Validate Inserts
            validate_insertion(cursor, expected_rows)
            
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()
            print("🔌 Connection closed.")

if __name__ == "__main__":
    print("\n\n*** STARTING SQL DATA LOADING PIPELINE ***")
    sleep(1) 
    main()
    