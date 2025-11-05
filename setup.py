#!/usr/bin/env python3
"""
Setup script for Sacramento SQL User Group Demo
Modernizing Database Testing: From Manual SQL to Intelligent Automation
"""

import sqlite3
import os
import sys

def create_demo_database():
    """Create and populate the demo SQLite database"""
    
    # Connect to SQLite database in current directory
    conn = sqlite3.connect('demo_database.db')
    cursor = conn.cursor()
    
    print("Creating demo database schema...")
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            registration_date DATE,
            loyalty_tier TEXT DEFAULT 'Bronze',
            total_spent DECIMAL(10,2) DEFAULT 0.00
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            amount DECIMAL(10,2),
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price DECIMAL(10,2),
            stock_quantity INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            unit_price DECIMAL(10,2),
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')
    
    print("Populating demo data...")
    
    # Sample customers
    customers = [
        (1, 'Alice Johnson', 'alice@email.com', '2023-01-15', 'Gold', 2500.00),
        (2, 'Bob Smith', 'bob@email.com', '2023-02-20', 'Silver', 1200.00),
        (3, 'Carol Davis', 'carol@email.com', '2023-03-10', 'Bronze', 450.00),
        (4, 'David Wilson', 'david@email.com', '2023-04-05', 'Platinum', 5000.00),
        (5, 'Eva Brown', 'eva@email.com', '2023-05-12', 'Gold', 3200.00),
        (6, 'Frank Miller', 'frank@email.com', '2023-06-01', 'Silver', 1800.00),
        (7, 'Grace Lee', 'grace@email.com', '2023-07-15', 'Bronze', 650.00),
        (8, 'Henry Garcia', 'henry@email.com', '2023-08-20', 'Platinum', 6200.00),
        (9, 'Iris Chen', 'iris@email.com', '2023-09-10', 'Gold', 2800.00),
        (10, 'Jack Thompson', 'jack@email.com', '2023-10-05', 'Silver', 1500.00)
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO customers (customer_id, name, email, registration_date, loyalty_tier, total_spent)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', customers)
    
    # Sample products
    products = [
        (1, 'Laptop Pro', 'Electronics', 1299.99, 50),
        (2, 'Wireless Headphones', 'Electronics', 199.99, 100),
        (3, 'Coffee Maker', 'Appliances', 89.99, 75),
        (4, 'Running Shoes', 'Sports', 129.99, 200),
        (5, 'Smartphone', 'Electronics', 799.99, 30),
        (6, 'Tablet', 'Electronics', 499.99, 40),
        (7, 'Blender', 'Appliances', 149.99, 60),
        (8, 'Yoga Mat', 'Sports', 39.99, 150),
        (9, 'Smart Watch', 'Electronics', 299.99, 80),
        (10, 'Air Fryer', 'Appliances', 119.99, 90)
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO products (product_id, name, category, price, stock_quantity)
        VALUES (?, ?, ?, ?, ?)
    ''', products)
    
    # Sample orders
    orders = [
        (1, 1, '2023-06-01', 1499.98, 'Completed'),
        (2, 2, '2023-06-02', 289.98, 'Completed'),
        (3, 3, '2023-06-03', 219.98, 'Pending'),
        (4, 4, '2023-06-04', 929.98, 'Completed'),
        (5, 5, '2023-06-05', 1099.98, 'Shipped'),
        (6, 6, '2023-06-06', 649.98, 'Completed'),
        (7, 7, '2023-06-07', 179.98, 'Pending'),
        (8, 8, '2023-06-08', 1599.98, 'Completed'),
        (9, 9, '2023-06-09', 799.98, 'Shipped'),
        (10, 10, '2023-06-10', 449.98, 'Completed')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO orders (order_id, customer_id, order_date, amount, status)
        VALUES (?, ?, ?, ?, ?)
    ''', orders)
    
    # Sample order items
    order_items = [
        (1, 1, 1, 1, 1299.99),  # Alice bought Laptop Pro
        (2, 1, 2, 1, 199.99),   # Alice bought Headphones
        (3, 2, 2, 1, 199.99),   # Bob bought Headphones
        (4, 2, 3, 1, 89.99),    # Bob bought Coffee Maker
        (5, 3, 4, 1, 129.99),   # Carol bought Running Shoes
        (6, 3, 3, 1, 89.99),    # Carol bought Coffee Maker
        (7, 4, 5, 1, 799.99),   # David bought Smartphone
        (8, 4, 4, 1, 129.99),   # David bought Running Shoes
        (9, 5, 6, 1, 499.99),   # Eva bought Tablet
        (10, 5, 9, 2, 299.99)   # Eva bought 2 Smart Watches
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO order_items (order_item_id, order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?, ?)
    ''', order_items)
    
    conn.commit()
    conn.close()
    
    print("✅ Demo database created successfully!")
    print("📍 Location: demo_database.db")

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], check=True, capture_output=True, text=True)
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        print("Please run manually: pip install -r requirements.txt")

def main():
    """Main setup function"""
    print("🚀 Setting up Sacramento SQL User Group Demo Environment")
    print("=" * 60)
    
    # Create demo database
    create_demo_database()
    
    # Install requirements
    install_requirements()
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the Streamlit app: streamlit run app.py")
    print("2. Open your browser to the provided URL")
    print("\n🎯 Demo Features:")
    print("• Interactive slide navigation")
    print("• Live SQL generation from natural language")
    print("• Synthetic data generation simulation")
    print("• End-to-end workflow demonstrations")
    print("• Real SQLite database integration")

if __name__ == "__main__":
    main()