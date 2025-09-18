#!/usr/bin/env python3
"""
Database connection test script for betterEngineer PostgreSQL setup.

Run this script to test your database connection and basic operations.
"""

import os
from dotenv import load_dotenv
from db import init_database, subscribe_user, get_active_users, unsubscribe_user, get_db

def test_database_connection():
    """Test database connection and basic operations."""
    print("🧪 Testing betterEngineer Database Connection...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    required_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASS"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Please check your .env file")
        return False
    
    print("✅ Environment variables loaded")
    
    # Test 1: Initialize database
    print("\n📊 Test 1: Database Initialization")
    try:
        if init_database():
            print("✅ Database tables initialized successfully")
        else:
            print("❌ Database initialization failed")
            return False
    except Exception as e:
        print(f"❌ Database initialization error: {str(e)}")
        return False
    
    # Test 2: Add a test subscriber
    print("\n👤 Test 2: Add Test Subscriber")
    test_email = "test@betterengineer.example"
    try:
        result = subscribe_user(test_email, "CSE", "weekly")
        if result["success"]:
            print(f"✅ Successfully added subscriber: {test_email}")
        else:
            print(f"❌ Failed to add subscriber: {result['error']}")
            if "already subscribed" not in result['error'].lower():
                return False
            else:
                print("   (Email already exists - this is expected)")
    except Exception as e:
        print(f"❌ Subscription error: {str(e)}")
        return False
    
    # Test 3: Get active subscribers
    print("\n📋 Test 3: Retrieve Active Subscribers")
    try:
        result = get_active_users()
        if result["success"]:
            print(f"✅ Successfully retrieved {result['count']} active subscribers")
            if result["data"]:
                print("   Sample subscriber data:")
                sample = result["data"][0]
                print(f"     - Email: {sample['email']}")
                print(f"     - Branch: {sample.get('branch', 'N/A')}")
                print(f"     - Frequency: {sample['frequency']}")
        else:
            print(f"❌ Failed to retrieve subscribers: {result['error']}")
            return False
    except Exception as e:
        print(f"❌ Retrieval error: {str(e)}")
        return False
    
    # Test 4: Get statistics
    print("\n📈 Test 4: Get Subscriber Statistics")
    try:
        db = get_db()
        result = db.get_subscriber_stats()
        if result["success"]:
            stats = result["stats"]
            print("✅ Successfully retrieved statistics:")
            print(f"     - Total Active: {stats['total_active']}")
            print(f"     - Total Unsubscribed: {stats['total_unsubscribed']}")
            print(f"     - Total All Time: {stats['total_all']}")
            print(f"     - Daily: {stats['frequency_breakdown']['daily']}")
            print(f"     - Weekly: {stats['frequency_breakdown']['weekly']}")
            print(f"     - Monthly: {stats['frequency_breakdown']['monthly']}")
        else:
            print(f"❌ Failed to get statistics: {result['error']}")
            return False
    except Exception as e:
        print(f"❌ Statistics error: {str(e)}")
        return False
    
    # Test 5: Test duplicate email handling
    print("\n🔄 Test 5: Duplicate Email Handling")
    try:
        result = subscribe_user(test_email, "ECE", "daily")
        if not result["success"] and "already subscribed" in result['error'].lower():
            print("✅ Duplicate email properly rejected")
        else:
            print("❌ Duplicate email handling failed")
            return False
    except Exception as e:
        print(f"❌ Duplicate test error: {str(e)}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All database tests passed successfully!")
    print("🚀 Your betterEngineer database is ready to use!")
    return True

if __name__ == "__main__":
    success = test_database_connection()
    
    if success:
        print("\n💡 Next steps:")
        print("   1. Run: streamlit run Home.py")
        print("   2. Test the subscription form")
        print("   3. Check the admin dashboard at /Admin")
    else:
        print("\n🔧 Troubleshooting:")
        print("   1. Check your .env file has all required variables")
        print("   2. Verify your database is running and accessible")
        print("   3. Run the database schema script")
        print("   4. Check the setup guide for your hosting provider")
    
    exit(0 if success else 1)
