"""
Load e-commerce CSV files into a SQLite database.
Creates tables: customers, products, orders, order_items, reviews
"""

import csv
import sqlite3
from pathlib import Path

# Database and data directory paths
DB_NAME = "ecommerce.db"
DATA_DIR = Path("data")

def create_tables(cursor):
    """Create all database tables with appropriate schemas."""
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            registration_date TEXT
        )
    """)
    
    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            cost REAL,
            stock_quantity INTEGER,
            description TEXT,
            brand TEXT,
            created_date TEXT
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            status TEXT,
            shipping_address TEXT,
            shipping_city TEXT,
            shipping_state TEXT,
            shipping_zip TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    # Create order_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price REAL,
            discount REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    
    # Create reviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY,
            product_id INTEGER,
            customer_id INTEGER,
            rating INTEGER,
            review_text TEXT,
            review_date TEXT,
            helpful_count INTEGER,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    print("Database tables created successfully.")

def load_csv_to_table(cursor, csv_file, table_name):
    """Load data from a CSV file into a database table."""
    csv_path = DATA_DIR / csv_file
    
    if not csv_path.exists():
        print(f"Warning: {csv_file} not found. Skipping...")
        return
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if not rows:
            print(f"Warning: {csv_file} is empty. Skipping...")
            return
        
        # Get column names from the first row
        columns = list(rows[0].keys())
        placeholders = ','.join(['?' for _ in columns])
        column_names = ','.join(columns)
        
        # Prepare insert statement
        insert_sql = f"INSERT OR REPLACE INTO {table_name} ({column_names}) VALUES ({placeholders})"
        
        # Insert rows
        for row in rows:
            values = [row[col] for col in columns]
            cursor.execute(insert_sql, values)
        
        print(f"Loaded {len(rows)} rows from {csv_file} into {table_name} table.")

def main():
    """Main function to load all CSV files into SQLite database."""
    print("=" * 60)
    print("Loading e-commerce CSV files into SQLite database...")
    print("=" * 60)
    
    # Connect to SQLite database (creates if doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Create all tables
        create_tables(cursor)
        print()
        
        # Load data in order (respecting foreign key constraints)
        # First load independent tables
        print("Loading data from CSV files...")
        print("-" * 60)
        load_csv_to_table(cursor, "customers.csv", "customers")
        load_csv_to_table(cursor, "products.csv", "products")
        
        # Then load dependent tables
        load_csv_to_table(cursor, "orders.csv", "orders")
        load_csv_to_table(cursor, "order_items.csv", "order_items")
        load_csv_to_table(cursor, "reviews.csv", "reviews")
        
        # Commit all changes
        conn.commit()
        print("-" * 60)
        print(f"\nSuccessfully loaded all CSV files into '{DB_NAME}' database!")
        
        # Display summary
        print("\n" + "=" * 60)
        print("Database Summary:")
        print("=" * 60)
        for table in ["customers", "products", "orders", "order_items", "reviews"]:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table:15} : {count:3} rows")
        print("=" * 60)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()
        print(f"\nDatabase connection closed.")

if __name__ == "__main__":
    main()

