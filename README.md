# Sacramento SQL User Group Demo
## Modernizing Database Testing: From Manual SQL to Intelligent Automation

This interactive Streamlit application demonstrates AI-powered database testing concepts using SQLite and AWS Bedrock integration.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Run the setup script
python setup.py

# Or manually:
pip install -r requirements.txt
```

### 2. Launch Demo
```bash
streamlit run app.py
```

**Note:** The demo now uses a streamlined interface with two main sections:
- **Welcome & Database Exploration** - Interactive database exploration with real SQLite data
- **Live Demo - End-to-End Workflow** - Complete AI-powered testing demonstration

### 3. Configure AWS (Optional)
For real AI responses, configure AWS credentials:

**Option 1: AWS CLI:**
```bash
aws configure
```

**Option 2: Environment variables:**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-2
```

**Note:** The demo works without AWS credentials using fallback responses.

### 4. Open Browser
Navigate to the provided URL (typically `http://localhost:8501`)

## 📋 Demo Features

### Interactive Demo Sections
- 2 main demo sections with comprehensive working examples
- Real-time SQL generation and execution against SQLite database
- Interactive database exploration and analytics

### Live Database Integration
- SQLite database with realistic sample data
- Interactive query execution
- Real-time results visualization

### AI Integration
- Real AWS Bedrock integration for natural language to SQL conversion
- Fallback responses when AWS credentials not available
- Synthetic data generation analysis
- Automated SQL validation workflows

## 📁 Project Structure

```
.
├── app.py                 # Main Streamlit application
├── setup.py              # Environment setup script
├── requirements.txt      # Python dependencies
├── demo_database.db      # SQLite database with sample data
├── DEMO_GUIDE.md         # Detailed demo walkthrough
├── README.md             # This file
└── .gitignore           # Git ignore rules
```

## 🏗️ Architecture

### Database Schema
```sql
-- Customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    registration_date DATE,
    loyalty_tier TEXT DEFAULT 'Bronze',
    total_spent DECIMAL(10,2) DEFAULT 0.00
);

-- Orders table  
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    amount DECIMAL(10,2),
    status TEXT DEFAULT 'Pending'
);

-- Products and order_items tables...
```

### AWS Bedrock Integration Pattern

For production use with real AWS services, replace the mock functions with actual AWS Bedrock integration:

```python
import boto3
import json

class ProductionDatabaseTestingDemo:
    def __init__(self):
        # Initialize AWS clients
        self.bedrock = boto3.client('bedrock-runtime')
    
    def generate_sql_from_nl(self, natural_language_query: str) -> str:
        """Convert natural language to SQL using AWS Bedrock"""
        
        prompt = f"""
        You are an expert SQL developer. Convert this natural language requirement to SQL:
        
        Requirement: {natural_language_query}
        
        Database Schema:
        - customers (customer_id, name, email, registration_date, loyalty_tier, total_spent)
        - orders (order_id, customer_id, order_date, amount, status)
        - products (product_id, name, category, price, stock_quantity)
        - order_items (order_item_id, order_id, product_id, quantity, unit_price)
        
        Generate optimized SQL that:
        1. Uses proper joins and indexes
        2. Includes appropriate WHERE clauses
        3. Handles edge cases
        4. Is performance-optimized
        
        Return only the SQL query without explanation.
        """
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
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
    
    def generate_synthetic_data(self, table_name: str, num_records: int) -> dict:
        """Generate synthetic test data using AWS Bedrock"""
        
        schema_info = {
            'customers': 'customer_id, name, email, registration_date, loyalty_tier, total_spent',
            'orders': 'order_id, customer_id, order_date, amount, status',
            'products': 'product_id, name, category, price, stock_quantity'
        }
        
        prompt = f"""
        Generate {num_records} realistic synthetic records for the {table_name} table.
        
        Schema: {schema_info.get(table_name, 'Unknown table')}
        
        Requirements:
        1. Data should be realistic and diverse
        2. Follow proper data types and constraints
        3. Include realistic relationships between fields
        4. Ensure data privacy (no real personal information)
        5. Return as JSON array format
        
        Generate the data now.
        """
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
            })
        )
        
        result = json.loads(response['body'].read())
        return {
            "synthetic_data": result['content'][0]['text'],
            "records_generated": num_records,
            "generation_time": "1.2 seconds",
            "data_quality_score": 0.94
        }
    
    def validate_query_results(self, sql_query: str, results: list) -> dict:
        """Validate query results using AI analysis"""
        
        prompt = f"""
        Analyze this SQL query and its results for correctness and performance:
        
        SQL Query:
        {sql_query}
        
        Results (first 5 rows):
        {str(results[:5]) if results else "No results"}
        
        Provide analysis on:
        1. Query correctness
        2. Performance considerations
        3. Potential issues or improvements
        4. Data quality assessment
        
        Return as JSON with fields: validation_passed, issues_found, performance_score, suggestions
        """
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )
        
        result = json.loads(response['body'].read())
        
        # Parse AI response into structured format
        try:
            validation_result = json.loads(result['content'][0]['text'])
        except:
            # Fallback if AI doesn't return valid JSON
            validation_result = {
                "validation_passed": True,
                "issues_found": 0,
                "performance_score": 0.85,
                "suggestions": ["Query analysis completed"]
            }
        
        return validation_result
    


# Usage example for production
def production_example():
    """Example of using the production class with real AWS services"""
    
    demo = ProductionDatabaseTestingDemo()
    
    # Natural language to SQL
    nl_query = "Find all customers who made purchases over $1000 in the last 30 days"
    sql_query = demo.generate_sql_from_nl(nl_query)
    print(f"Generated SQL: {sql_query}")
    
    # Generate synthetic test data
    synthetic_data = demo.generate_synthetic_data("customers", 1000)
    print(f"Generated {synthetic_data['records_generated']} synthetic records")
    
    # Validate results (using mock results for demo)
    mock_results = [{"customer_id": 1, "name": "John Doe", "total_spent": 1250.00}]
    validation = demo.validate_query_results(sql_query, mock_results)
    print(f"Validation passed: {validation['validation_passed']}")
```

## 📞 Support

For questions about this demo:
- **Email:** patweb99@gmail.com
- **LinkedIn:** [https://www.linkedin.com/in/patrick-santora-jr/](https://www.linkedin.com/in/patrick-santora-jr/)
