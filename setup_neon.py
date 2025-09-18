#!/usr/bin/env python3
"""
Neon.tech PostgreSQL database setup script.
Run this after updating your .env file with Neon credentials.
"""

import os
import psycopg2
from dotenv import load_dotenv

def setup_neon_database():
    """Set up the database schema on Neon PostgreSQL."""
    print("🌟 Setting up Neon PostgreSQL Database (Free Forever)")
    print("=" * 55)
    
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
        print("   Please update .env with your Neon database details")
        print("\n📋 Steps to get Neon credentials:")
        print("   1. Go to https://neon.tech")
        print("   2. Sign up with GitHub (free)")
        print("   3. Create project 'betterengineer'")
        print("   4. Copy connection string")
        print("   5. Update .env file")
        return False
    
    try:
        # Connect to Neon PostgreSQL
        print(f"🔌 Connecting to Neon database at {db_host}...")
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass,
            port=db_port,
            sslmode='require'  # Neon requires SSL
        )
        
        cursor = conn.cursor()
        print("✅ Successfully connected to Neon PostgreSQL!")
        
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
        
        # Show Neon-specific info
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"📊 PostgreSQL version: {version.split(',')[0]}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 55)
        print("🎉 Neon PostgreSQL setup complete!")
        print("🚀 Your FREE production database is ready!")
        print("💚 Neon will auto-sleep when unused (saves resources)")
        print("⚡ Auto-wakes instantly on first query")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {str(e)}")
        print("\n🔧 Common solutions:")
        print("   1. Check your Neon credentials in .env file")
        print("   2. Ensure your Neon project is active")
        print("   3. Verify the connection string is correct")
        print("   4. Try copying the connection string again")
        return False
    except FileNotFoundError:
        print("❌ database_schema.sql file not found")
        print("   Make sure you're running this from the project root")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = setup_neon_database()
    
    if success:
        print("\n💡 Next steps:")
        print("   1. Run: uv run python test_db.py")
        print("   2. Run: uv run streamlit run Home.py")
        print("   3. Test the subscription form")
        print("   4. Your app is production-ready on Neon's free tier!")
        print("\n🌟 Neon Free Tier Benefits:")
        print("   • 3GB storage (enough for 100k+ subscribers)")
        print("   • Auto-sleep when unused")
        print("   • Instant wake-up")
        print("   • No time limits or trials!")
    else:
        print("\n🔧 Need help? Follow these steps:")
        print("   1. Go to https://neon.tech")
        print("   2. Sign up with GitHub")
        print("   3. Create project 'betterengineer'")
        print("   4. Copy the connection string")
        print("   5. Update your .env file")
        print("   6. Run this script again")
    
    exit(0 if success else 1)
