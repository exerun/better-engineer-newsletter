#!/usr/bin/env python3
"""
Railway PostgreSQL database setup script.
Run this after updating your .env file with Railway credentials.
"""

import os
import psycopg2
from dotenv import load_dotenv

def setup_railway_database():
    """Set up the database schema on Railway PostgreSQL."""
    print("🚂 Setting up Railway PostgreSQL Database")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get database credentials
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_port = os.getenv("DB_PORT", 5432)
    
    if not all([db_host, db_name, db_user, db_pass]):
        print("❌ Missing database credentials in .env file")
        print("   Please update .env with your Railway database details")
        return False
    
    try:
        # Connect to Railway PostgreSQL
        print(f"🔌 Connecting to Railway database at {db_host}...")
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass,
            port=db_port,
            sslmode='require'  # Railway requires SSL
        )
        
        cursor = conn.cursor()
        print("✅ Successfully connected to Railway PostgreSQL!")
        
        # Read and execute schema
        print("📋 Setting up database schema...")
        with open('database_schema.sql', 'r') as file:
            schema_sql = file.read()
        
        # Execute schema creation
        cursor.execute(schema_sql)
        conn.commit()
        print("✅ Database schema created successfully!")
        
        # Test the setup with a sample query
        print("🧪 Testing database setup...")
        cursor.execute("SELECT COUNT(*) FROM subscribers;")
        count = cursor.fetchone()[0]
        print(f"✅ Subscribers table ready (current count: {count})")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 50)
        print("🎉 Railway PostgreSQL setup complete!")
        print("🚀 Your production database is ready!")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {str(e)}")
        print("   Check your Railway credentials in .env file")
        return False
    except FileNotFoundError:
        print("❌ database_schema.sql file not found")
        print("   Make sure you're running this from the project root")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = setup_railway_database()
    
    if success:
        print("\n💡 Next steps:")
        print("   1. Run: uv run python test_db.py")
        print("   2. Run: uv run streamlit run Home.py")
        print("   3. Test the subscription form")
        print("   4. Deploy to Railway for public access")
    else:
        print("\n🔧 Troubleshooting:")
        print("   1. Verify Railway database is running")
        print("   2. Check .env file has correct credentials")
        print("   3. Ensure you copied the connection details correctly")
        print("   4. Try connecting with railway CLI: railway connect")
    
    exit(0 if success else 1)
