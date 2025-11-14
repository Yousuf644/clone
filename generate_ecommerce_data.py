"""
Generate synthetic e-commerce CSV files with realistic sample data.
Creates: customers.csv, products.csv, orders.csv, order_items.csv, reviews.csv
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Set random seed for reproducibility
random.seed(42)

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Sample data pools
first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
               "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
               "Thomas", "Sarah", "Christopher", "Karen", "Daniel", "Nancy", "Matthew", "Lisa"]

last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
              "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor"]

product_names = [
    "Wireless Bluetooth Headphones", "Smartphone Case - Clear", "USB-C Charging Cable",
    "Laptop Stand - Adjustable", "Wireless Mouse - Ergonomic", "Mechanical Keyboard - RGB",
    "Monitor Stand - Dual", "Desk Organizer - Bamboo", "Webcam HD 1080p", "USB Hub - 4 Port",
    "Laptop Sleeve - Neoprene", "Screen Protector - Anti-Glare", "Cable Management Kit",
    "Desk Lamp - LED", "Laptop Cooling Pad", "External Hard Drive 1TB", "USB Flash Drive 64GB",
    "Wireless Charger - Fast", "Phone Stand - Adjustable", "Bluetooth Speaker - Portable"
]

product_categories = ["Electronics", "Accessories", "Computer", "Mobile", "Audio", "Storage", "Office"]

# Generate customers.csv
def generate_customers():
    customers = []
    for i in range(1, 16):  # 15 customers
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{i}@email.com"
        phone = f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
        address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Elm', 'Park', 'Maple'])} St"
        city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio"])
        state = random.choice(["NY", "CA", "IL", "TX", "AZ", "PA", "FL"])
        zip_code = f"{random.randint(10000, 99999)}"
        registration_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d")
        
        customers.append({
            "customer_id": i,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "registration_date": registration_date
        })
    
    with open(data_dir / "customers.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)
    print(f"Generated customers.csv with {len(customers)} rows")

# Generate products.csv
def generate_products():
    products = []
    for i in range(1, 18):  # 17 products
        name = product_names[i-1] if i <= len(product_names) else f"Product {i}"
        category = random.choice(product_categories)
        price = round(random.uniform(9.99, 299.99), 2)
        cost = round(price * random.uniform(0.4, 0.7), 2)
        stock_quantity = random.randint(0, 500)
        description = f"High-quality {name.lower()} perfect for your needs."
        brand = random.choice(["TechBrand", "ProTech", "SmartGear", "EliteTech", "PrimeTech"])
        created_date = (datetime.now() - timedelta(days=random.randint(1, 730))).strftime("%Y-%m-%d")
        
        products.append({
            "product_id": i,
            "name": name,
            "category": category,
            "price": price,
            "cost": cost,
            "stock_quantity": stock_quantity,
            "description": description,
            "brand": brand,
            "created_date": created_date
        })
    
    with open(data_dir / "products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    print(f"Generated products.csv with {len(products)} rows")

# Generate orders.csv
def generate_orders():
    orders = []
    order_id = 1
    for customer_id in range(1, 16):  # 15 customers
        # Each customer has 0-3 orders
        num_orders = random.randint(0, 3)
        for _ in range(num_orders):
            order_date = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")
            status = random.choice(["Pending", "Processing", "Shipped", "Delivered", "Cancelled"])
            shipping_address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Elm', 'Park'])} St"
            shipping_city = random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"])
            shipping_state = random.choice(["NY", "CA", "IL", "TX", "AZ"])
            shipping_zip = f"{random.randint(10000, 99999)}"
            
            orders.append({
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date,
                "status": status,
                "shipping_address": shipping_address,
                "shipping_city": shipping_city,
                "shipping_state": shipping_state,
                "shipping_zip": shipping_zip
            })
            order_id += 1
    
    # Ensure we have at least 10 orders
    while len(orders) < 10:
        customer_id = random.randint(1, 15)
        order_date = (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")
        status = random.choice(["Pending", "Processing", "Shipped", "Delivered"])
        shipping_address = f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Elm'])} St"
        shipping_city = random.choice(["New York", "Los Angeles", "Chicago"])
        shipping_state = random.choice(["NY", "CA", "IL"])
        shipping_zip = f"{random.randint(10000, 99999)}"
        
        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": status,
            "shipping_address": shipping_address,
            "shipping_city": shipping_city,
            "shipping_state": shipping_state,
            "shipping_zip": shipping_zip
        })
        order_id += 1
    
    with open(data_dir / "orders.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)
    print(f"Generated orders.csv with {len(orders)} rows")
    return [order["order_id"] for order in orders]

# Generate order_items.csv
def generate_order_items(order_ids):
    order_items = []
    item_id = 1
    
    for order_id in order_ids:
        # Each order has 1-4 items
        num_items = random.randint(1, 4)
        products_in_order = random.sample(range(1, 18), min(num_items, 17))
        
        for product_id in products_in_order:
            quantity = random.randint(1, 3)
            unit_price = round(random.uniform(9.99, 299.99), 2)
            discount = round(random.uniform(0, 0.25), 2) if random.random() < 0.3 else 0.0
            
            order_items.append({
                "item_id": item_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount
            })
            item_id += 1
    
    with open(data_dir / "order_items.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=order_items[0].keys())
        writer.writeheader()
        writer.writerows(order_items)
    print(f"Generated order_items.csv with {len(order_items)} rows")
    return [item["product_id"] for item in order_items]

# Generate reviews.csv
def generate_reviews(order_ids, product_ids):
    reviews = []
    review_id = 1
    
    # Generate reviews for some products
    reviewed_products = list(set(product_ids))[:15]  # Review up to 15 unique products
    
    for product_id in reviewed_products:
        # Each product gets 1-2 reviews
        num_reviews = random.randint(1, 2)
        for _ in range(num_reviews):
            customer_id = random.randint(1, 15)
            rating = random.choices([1, 2, 3, 4, 5], weights=[1, 2, 3, 15, 20])[0]  # Bias toward higher ratings
            review_texts = [
                "Great product! Highly recommend.",
                "Good quality and fast shipping.",
                "Exactly as described. Very satisfied.",
                "Not bad, but could be better.",
                "Excellent value for money!",
                "Works perfectly for my needs.",
                "Good product, but shipping took a while.",
                "Amazing quality! Will buy again.",
                "Decent product, meets expectations.",
                "Outstanding! Exceeded my expectations.",
                "Good product overall, minor issues.",
                "Perfect! Exactly what I needed.",
                "Very happy with this purchase.",
                "Could be improved, but acceptable.",
                "Top quality product, highly recommended!"
            ]
            review_text = random.choice(review_texts)
            review_date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
            helpful_count = random.randint(0, 25)
            
            reviews.append({
                "review_id": review_id,
                "product_id": product_id,
                "customer_id": customer_id,
                "rating": rating,
                "review_text": review_text,
                "review_date": review_date,
                "helpful_count": helpful_count
            })
            review_id += 1
    
    # Ensure we have at least 10 reviews
    while len(reviews) < 10:
        product_id = random.randint(1, 17)
        customer_id = random.randint(1, 15)
        rating = random.randint(1, 5)
        review_text = random.choice([
            "Great product! Highly recommend.",
            "Good quality and fast shipping.",
            "Exactly as described. Very satisfied.",
            "Excellent value for money!",
            "Works perfectly for my needs."
        ])
        review_date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
        helpful_count = random.randint(0, 20)
        
        reviews.append({
            "review_id": review_id,
            "product_id": product_id,
            "customer_id": customer_id,
            "rating": rating,
            "review_text": review_text,
            "review_date": review_date,
            "helpful_count": helpful_count
        })
        review_id += 1
    
    with open(data_dir / "reviews.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reviews[0].keys())
        writer.writeheader()
        writer.writerows(reviews)
    print(f"Generated reviews.csv with {len(reviews)} rows")

# Main execution
if __name__ == "__main__":
    print("Generating synthetic e-commerce CSV files...")
    print("-" * 50)
    
    generate_customers()
    generate_products()
    order_ids = generate_orders()
    product_ids = generate_order_items(order_ids)
    generate_reviews(order_ids, product_ids)
    
    print("-" * 50)
    print(f"All CSV files generated successfully in '{data_dir}' folder!")
