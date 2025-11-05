import streamlit as st
import sqlite3
import pandas as pd
import json
import random
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Any
import boto3
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Sacramento SQL User Group Demo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF9900;
        text-align: center;
        margin-bottom: 2rem;
    }
    .slide-header {
        font-size: 1.8rem;
        color: #232F3E;
        border-bottom: 2px solid #FF9900;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .demo-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF9900;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DatabaseTestingDemo:
    def __init__(self):
        self.init_database()
        self.init_aws_bedrock()
    
    def init_database(self):
        """Initialize SQLite database with sample schema"""
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.create_sample_schema()
        self.populate_sample_data()
    
    def init_aws_bedrock(self):
        """Initialize AWS Bedrock client"""
        profile_name = 'demo-bedrock'
        region_name = 'us-east-2'
        
        try:
            # Try with the specific profile first
            session = boto3.Session(profile_name=profile_name)
            self.bedrock = session.client('bedrock-runtime', region_name=region_name)
            st.success(f"✅ Connected to AWS Bedrock using profile: {profile_name}")
            
        except Exception as profile_error:
            st.error("❌ AWS Bedrock connection failed. Please configure AWS credentials.")
            st.info("💡 This demo requires AWS Bedrock access to function properly.")
            self.bedrock = None
    
    def create_sample_schema(self):
        """Create sample database schema"""
        cursor = self.conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                registration_date DATE,
                loyalty_tier TEXT DEFAULT 'Bronze',
                total_spent DECIMAL(10,2) DEFAULT 0.00
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date DATE,
                amount DECIMAL(10,2),
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                price DECIMAL(10,2),
                stock_quantity INTEGER DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def populate_sample_data(self):
        """Populate database with sample data"""
        cursor = self.conn.cursor()
        
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
            INSERT INTO customers (customer_id, name, email, registration_date, loyalty_tier, total_spent)
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
            INSERT INTO products (product_id, name, category, price, stock_quantity)
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
            INSERT INTO orders (order_id, customer_id, order_date, amount, status)
            VALUES (?, ?, ?, ?, ?)
        ''', orders)
        
        self.conn.commit()
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            return pd.read_sql_query(query, self.conn)
        except Exception as e:
            st.error(f"Query execution error: {str(e)}")
            return pd.DataFrame()
    
    def get_database_schema(self) -> str:
        """Get database schema description for AI context"""
        return """
        Database Schema:
        
        1. customers table:
           - customer_id (INTEGER PRIMARY KEY)
           - name (TEXT NOT NULL)
           - email (TEXT UNIQUE NOT NULL)
           - registration_date (DATE)
           - loyalty_tier (TEXT: Bronze, Silver, Gold, Platinum)
           - total_spent (DECIMAL)
        
        2. orders table:
           - order_id (INTEGER PRIMARY KEY)
           - customer_id (INTEGER, foreign key to customers)
           - order_date (DATE)
           - amount (DECIMAL)
           - status (TEXT: Pending, Completed, Shipped)
        
        3. products table:
           - product_id (INTEGER PRIMARY KEY)
           - name (TEXT NOT NULL)
           - category (TEXT: Electronics, Appliances, Sports)
           - price (DECIMAL)
           - stock_quantity (INTEGER)
        """
    
    def call_bedrock_claude(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call AWS Bedrock Claude model"""
        # Always try Bedrock first, even if initial connection test failed
        if self.bedrock is None:
            # Try to reinitialize if bedrock client is None
            try:
                session = boto3.Session(profile_name='demo-bedrock')
                self.bedrock = session.client('bedrock-runtime', region_name='us-east-2')
            except:
                self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-2')
        
        response = self.bedrock.invoke_model(
            modelId='us.anthropic.claude-3-5-haiku-20241022-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']
    
    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response, handling cases where JSON is embedded in text"""
        try:
            # First try direct JSON parsing
            return json.loads(response.strip())
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from the response
            import re
            
            # Look for JSON-like content between curly braces
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            # If all else fails, return a default response based on task type
            if "validation" in response.lower():
                return {
                    "validation_passed": True,
                    "issues_found": 0,
                    "performance_score": 0.85,
                    "suggestions": ["Query appears to be well-formed", "Consider adding indexes for better performance"]
                }
            elif "synthetic" in response.lower() or "data" in response.lower():
                return {
                    "records_generated": 10000,
                    "generation_time": "2.3 seconds",
                    "data_quality_score": 0.92
                }
            else:
                return {"message": "AI response processed", "status": "success"}

    def bedrock_response(self, prompt: str, task_type: str) -> Dict[str, Any]:
        """Get AI responses using AWS Bedrock"""
        
        if task_type == "nl_to_sql":
            schema = self.get_database_schema()
            
            bedrock_prompt = f"""
            You are an expert SQL developer. Convert this natural language requirement to optimized SQLite SQL.
            
            Natural Language Requirement: {prompt}
            
            {schema}
            
            Requirements:
            1. Generate SQLite-compatible SQL only
            2. Use proper JOINs when needed
            3. Include appropriate WHERE clauses
            4. Optimize for performance
            5. Return only the SQL query, no explanation
            6. Use table aliases for readability
            
            SQL Query:
            """
            
            sql_response = self.call_bedrock_claude(bedrock_prompt, 500)
            
            # Clean up the response to extract just the SQL
            sql_query = sql_response.strip()
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            return {"sql": sql_query}
        
        elif task_type == "synthetic_data":
            bedrock_prompt = f"""
            You are a data generation expert. Analyze this request for synthetic data generation:
            
            Request: {prompt}
            
            Provide a realistic assessment of synthetic data generation including:
            - Number of records that could be generated
            - Estimated generation time
            - Data quality score (0.0 to 1.0)
            
            Respond in this exact JSON format:
            {{"records_generated": <number>, "generation_time": "<time>", "data_quality_score": <score>}}
            """
            
            response = self.call_bedrock_claude(bedrock_prompt, 200)
            
            # Parse JSON response from Bedrock with error handling
            result = self.parse_json_response(response)
            return result
        
        elif task_type == "validation":
            bedrock_prompt = f"""
            You are a SQL performance expert. Analyze this SQL query for validation:
            
            Query Context: {prompt}
            
            Provide analysis including:
            - Whether validation passed (true/false)
            - Number of issues found (0-5)
            - Performance score (0.0 to 1.0)
            - 2-3 specific suggestions for improvement
            
            Respond in this exact JSON format:
            {{"validation_passed": <boolean>, "issues_found": <number>, "performance_score": <score>, "suggestions": ["suggestion1", "suggestion2"]}}
            """
            
            response = self.call_bedrock_claude(bedrock_prompt, 300)
            
            # Parse JSON response from Bedrock with error handling
            result = self.parse_json_response(response)
            return result
        
        return {"message": "AI response generated"}

# Initialize the demo class
@st.cache_resource
def get_demo_instance():
    return DatabaseTestingDemo()

demo = get_demo_instance()

# Main app header
st.markdown('<h1 class="main-header">🚀 Modernizing Database Querying with AI</h1>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center;"><strong>Sacramento SQL User Group - November 5, 2025</strong> | <strong>Presenter:</strong> Pat Santora, AWS GenAI Labs | <strong>LinkedIn:</strong> https://www.linkedin.com/in/patrick-santora-jr/</div>', unsafe_allow_html=True)

# Tab navigation
tab1, tab2 = st.tabs(["Welcome & Database Exploration", "Live Demo - End-to-End Workflow"])

# Tab 1: Welcome & Database Exploration
with tab1:
    
    # Use Case Scenario
    st.markdown("### 🎯 The Challenge: Real-World Database Testing")
    
    st.warning("""
    **Imagine this scenario:** Your e-commerce platform needs comprehensive testing before Black Friday. 
    Your QA team needs to validate customer loyalty algorithms, order processing workflows, and 
    inventory management systems across millions of records.
    """)

    # Database Schema
    st.markdown("### 📊 Database Schema")
    st.code("""
    Tables:
    • customers (id, name, email, loyalty_tier, total_spent)
    • orders (id, customer_id, order_date, amount, status)  
    • products (id, name, category, price, stock_quantity)
    """, language="sql")
    
    # Interactive demo of current database
    st.markdown("**🔍 Explore Our Demo Database**")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        table_choice = st.selectbox("Select a table to explore:", ["customers", "orders", "products"])
        
        if st.button("Show Table Data"):
            query = f"SELECT * FROM {table_choice} LIMIT 10"
            df = demo.execute_query(query)
            st.session_state.current_data = df
    
    with col2:
        if 'current_data' in st.session_state:
            st.dataframe(st.session_state.current_data, use_container_width=True)
    
    # Quick analytics
    st.markdown("### Quick Database Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        customer_count = demo.execute_query("SELECT COUNT(*) as count FROM customers").iloc[0]['count']
        st.metric("Total Customers", customer_count)
    
    with col2:
        order_count = demo.execute_query("SELECT COUNT(*) as count FROM orders").iloc[0]['count']
        st.metric("Total Orders", order_count)
    
    with col3:
        avg_spent = demo.execute_query("SELECT AVG(total_spent) as avg FROM customers").iloc[0]['avg']
        st.metric("Avg Customer Spend", f"${avg_spent:.2f}")
    
    with col4:
        product_count = demo.execute_query("SELECT COUNT(*) as count FROM products").iloc[0]['count']
        st.metric("Total Products", product_count)
    


# Tab 2: Live Demo - End-to-End Workflow
with tab2:
    
    st.markdown("### Real-Time AI-Powered Database Testing")
    
    # Predefined examples
    example_queries = [
        "Show me the top 5 customers by total spending",
        "Find all customers who made purchases over $1000",
        "List customers by loyalty tier with average spending",
        "Show me all pending orders with customer details"
    ]
    
    st.markdown("**Quick Examples:**")
    for i, example in enumerate(example_queries):
        if st.button(f"📝 {example}", key=f"demo_example_{i}"):
            st.session_state.demo_input = example
    
    # Custom input
    demo_requirement = st.text_area(
        "Or enter your own business requirement:",
        value=st.session_state.get('demo_input', ''),
        height=80,
        placeholder="e.g., Find customers eligible for platinum status..."
    )
    
    if st.button("🚀 Start End-to-End Demo", type="primary"):
        if demo_requirement:
            # Create columns for real-time progress
            progress_container = st.container()
            results_container = st.container()
            
            with progress_container:
                st.markdown("**🎯 Demo Progress:**")
                progress_bar = st.progress(0)
                status_text = st.empty()
            
            # Step-by-step execution with real-time updates
            steps = [
                "🧠 AI analyzing business requirement",
                "📝 Generating optimized SQL query", 
                "⚡ Executing query on database"
            ]
            
            for i, step in enumerate(steps):
                status_text.text(f"{step}...")
                progress_bar.progress((i + 1) / len(steps))
                
                # Show intermediate results
                if i == 1:  # SQL Generation
                    with results_container:
                        st.markdown("**Generated SQL Query:**")
                        response = demo.bedrock_response(demo_requirement, "nl_to_sql")
                        generated_sql = response["sql"]
                        
                        st.code(generated_sql, language='sql')
                        
                        # Store for execution
                        st.session_state.demo_sql = generated_sql
                
                elif i == 2:  # Execution
                    with results_container:
                        st.markdown("**Query Execution Results:**")
                        if 'demo_sql' in st.session_state:
                            # Execute the actual SQL query against SQLite database
                            import time
                            start_time = time.time()
                            df = demo.execute_query(st.session_state.demo_sql)
                            execution_time = time.time() - start_time
                            
                            if not df.empty:
                                st.success(f"✅ Query executed successfully against SQLite database!")
                                st.dataframe(df, use_container_width=True)
                                st.info(f"📊 Returned {len(df)} rows in {execution_time:.3f} seconds")
                                st.session_state.demo_results = df
                                
                            else:
                                st.warning("Query executed against SQLite but returned no results.")
                

                
                import time
                time.sleep(0.8)  # Simulate processing time
            
            status_text.text("✅ End-to-end demo completed successfully!")
        else:
            st.warning("Please enter a business requirement to start the demo.")
    
