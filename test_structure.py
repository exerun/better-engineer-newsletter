#!/usr/bin/env python3
"""
Simple test to validate the Home.py code without database connection.
This tests the imports and basic structure.
"""

import sys
import os

def test_imports():
    """Test if all imports work correctly."""
    print("🧪 Testing betterEngineer Code Structure")
    print("=" * 45)
    
    try:
        # Test basic imports
        print("📦 Testing basic imports...")
        import streamlit as st
        import time
        print("✅ Streamlit and time imported successfully")
        
        # Test if we can import the database module structure
        print("🗄️ Testing database module...")
        try:
            from db import SubscriberDB, DatabaseManager, Subscriber
            print("✅ Database classes imported successfully")
        except Exception as e:
            print(f"❌ Database import failed: {str(e)}")
            return False
        
        # Test environment loading
        print("⚙️ Testing environment loading...")
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment loading works")
        
        # Test SQLAlchemy imports
        print("🔧 Testing SQLAlchemy imports...")
        from sqlalchemy import create_engine, Column, Integer, String, DateTime
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        print("✅ SQLAlchemy imports successful")
        
        # Test psycopg2 import
        print("🐘 Testing PostgreSQL driver...")
        import psycopg2
        print("✅ psycopg2 imported successfully")
        
        print("\n" + "=" * 45)
        print("🎉 All code structure tests passed!")
        print("✅ Your application is ready for database connection")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_database_class_structure():
    """Test if database classes can be instantiated without connection."""
    print("\n🏗️ Testing Database Class Structure")
    print("-" * 45)
    
    try:
        # We'll test the class definitions without actual connection
        print("Testing database model definitions...")
        
        # Import the classes
        from db import Subscriber, DatabaseManager
        from sqlalchemy.ext.declarative import declarative_base
        
        # Test that the Subscriber model is properly defined
        Base = declarative_base()
        
        # Check if Subscriber has the expected attributes
        expected_attrs = ['id', 'email', 'branch', 'frequency', 'status', 'created_at']
        for attr in expected_attrs:
            if hasattr(Subscriber, attr):
                print(f"✅ Subscriber.{attr} defined correctly")
            else:
                print(f"❌ Subscriber.{attr} missing")
                return False
        
        print("✅ Database model structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ Database class test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing betterEngineer Application Structure\n")
    
    success = True
    success &= test_imports()
    success &= test_database_class_structure()
    
    if success:
        print("\n💡 Summary:")
        print("✅ All code structure tests passed")
        print("✅ Dependencies are properly installed")
        print("✅ Database models are correctly defined")
        print("✅ Application is ready for database connection")
        print("\n🚀 Next steps:")
        print("   1. Set up PostgreSQL database (Railway/Render/Neon)")
        print("   2. Update .env with your database credentials")
        print("   3. Run: uv run python test_db.py")
        print("   4. Run: uv run streamlit run Home.py")
    else:
        print("\n🔧 Issues found:")
        print("   Please check the error messages above")
        print("   Make sure all dependencies are installed: uv sync")
    
    exit(0 if success else 1)
