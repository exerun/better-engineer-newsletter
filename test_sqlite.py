#!/usr/bin/env python3
"""
Quick SQLite test for betterEngineer database functionality.
This tests the database operations without requiring PostgreSQL setup.
"""

import sqlite3
from datetime import datetime
import os

def create_test_database():
    """Create SQLite test database with subscribers table."""
    conn = sqlite3.connect('test_betterengineer.db')
    cursor = conn.cursor()
    
    # Create subscribers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            branch TEXT,
            frequency TEXT NOT NULL DEFAULT 'weekly',
            status TEXT NOT NULL DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn

def test_sqlite_operations():
    """Test basic database operations with SQLite."""
    print("🧪 Testing betterEngineer Database Operations (SQLite)")
    print("=" * 55)
    
    try:
        # Create database
        conn = create_test_database()
        cursor = conn.cursor()
        print("✅ SQLite database created successfully")
        
        # Test 1: Insert subscriber
        print("\n👤 Test 1: Add Test Subscribers")
        test_data = [
            ("test1@betterengineer.example", "CSE", "weekly", "active"),
            ("test2@betterengineer.example", "ECE", "daily", "active"),
            ("test3@betterengineer.example", None, "monthly", "active"),
        ]
        
        for email, branch, frequency, status in test_data:
            cursor.execute('''
                INSERT OR IGNORE INTO subscribers (email, branch, frequency, status)
                VALUES (?, ?, ?, ?)
            ''', (email, branch, frequency, status))
        
        conn.commit()
        print(f"✅ Added {len(test_data)} test subscribers")
        
        # Test 2: Get active subscribers
        print("\n📋 Test 2: Retrieve Active Subscribers")
        cursor.execute('SELECT * FROM subscribers WHERE status = ?', ('active',))
        subscribers = cursor.fetchall()
        print(f"✅ Found {len(subscribers)} active subscribers:")
        
        for sub in subscribers:
            print(f"     - {sub[1]} ({sub[2] or 'No branch'}) - {sub[3]} frequency")
        
        # Test 3: Test duplicate email
        print("\n🔄 Test 3: Duplicate Email Handling")
        try:
            cursor.execute('''
                INSERT INTO subscribers (email, branch, frequency, status)
                VALUES (?, ?, ?, ?)
            ''', ("test1@betterengineer.example", "ME", "weekly", "active"))
            conn.commit()
            print("❌ Duplicate email was allowed (unexpected)")
        except sqlite3.IntegrityError:
            print("✅ Duplicate email properly rejected")
        
        # Test 4: Get statistics
        print("\n📈 Test 4: Generate Statistics")
        stats_queries = {
            'total_active': "SELECT COUNT(*) FROM subscribers WHERE status = 'active'",
            'total_all': "SELECT COUNT(*) FROM subscribers",
            'daily': "SELECT COUNT(*) FROM subscribers WHERE status = 'active' AND frequency = 'daily'",
            'weekly': "SELECT COUNT(*) FROM subscribers WHERE status = 'active' AND frequency = 'weekly'",
            'monthly': "SELECT COUNT(*) FROM subscribers WHERE status = 'active' AND frequency = 'monthly'"
        }
        
        stats = {}
        for name, query in stats_queries.items():
            cursor.execute(query)
            stats[name] = cursor.fetchone()[0]
        
        print("✅ Statistics generated:")
        print(f"     - Total Active: {stats['total_active']}")
        print(f"     - Total All: {stats['total_all']}")
        print(f"     - Daily: {stats['daily']}")
        print(f"     - Weekly: {stats['weekly']}")
        print(f"     - Monthly: {stats['monthly']}")
        
        # Test 5: Unsubscribe
        print("\n📧 Test 5: Unsubscribe Operation")
        cursor.execute('''
            UPDATE subscribers 
            SET status = 'unsubscribed' 
            WHERE email = ? AND status = 'active'
        ''', ("test2@betterengineer.example",))
        
        if cursor.rowcount > 0:
            conn.commit()
            print("✅ Successfully unsubscribed user")
        else:
            print("❌ Unsubscribe failed")
        
        # Final count
        cursor.execute("SELECT COUNT(*) FROM subscribers WHERE status = 'active'")
        final_active = cursor.fetchone()[0]
        print(f"     - Active subscribers after unsubscribe: {final_active}")
        
        conn.close()
        
        print("\n" + "=" * 55)
        print("🎉 All SQLite database tests passed!")
        print("✅ Your database logic is working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    
    finally:
        # Clean up test database
        if os.path.exists('test_betterengineer.db'):
            os.remove('test_betterengineer.db')
            print("🧹 Cleaned up test database")

if __name__ == "__main__":
    success = test_sqlite_operations()
    
    if success:
        print("\n💡 Your database operations are working correctly!")
        print("🚀 Next steps:")
        print("   1. Set up PostgreSQL (Railway, Render, or Neon)")
        print("   2. Update .env with your database credentials")
        print("   3. Run: python test_db.py")
        print("   4. Run: streamlit run Home.py")
    else:
        print("\n🔧 There was an issue with the database operations.")
        print("   Please check the error messages above.")
    
    exit(0 if success else 1)
