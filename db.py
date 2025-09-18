"""
Database layer for betterEngineer Newsletter using PostgreSQL with SQLAlchemy.

This module provides all database operations for managing newsletter subscribers
with connection pooling and production-ready error handling.
"""

import os
from typing import List, Dict, Optional, Any
from datetime import datetime
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
Base = declarative_base()

class Subscriber(Base):
    """SQLAlchemy model for subscribers table."""
    __tablename__ = 'subscribers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    branch = Column(String, nullable=True)
    frequency = Column(String, nullable=False, default='weekly')
    status = Column(String, nullable=False, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseManager:
    """Database connection and session management."""
    
    def __init__(self):
        """Initialize database connection with connection pooling."""
        self.engine = None
        self.SessionLocal = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database connection and session factory."""
        try:
            # Get database credentials from environment
            db_host = os.getenv("DB_HOST")
            db_name = os.getenv("DB_NAME")
            db_user = os.getenv("DB_USER")
            db_pass = os.getenv("DB_PASS")
            db_port = os.getenv("DB_PORT", "5432")
            
            if not all([db_host, db_name, db_user, db_pass]):
                raise ValueError("Missing required database environment variables")
            
            # Create connection string
            connection_string = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
            
            # Create engine with connection pooling
            self.engine = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=3600,   # Recycle connections every hour
                echo=False  # Set to True for SQL debugging
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Test connection
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                
        except Exception as e:
            st.error(f"❌ Database connection failed: {str(e)}")
            st.info("Please check your database environment variables in the .env file.")
            st.stop()
    
    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()
    
    def close(self):
        """Close database connections."""
        if self.engine:
            self.engine.dispose()

# Global database manager instance
db_manager = DatabaseManager()

class SubscriberDB:
    """Database operations for newsletter subscribers."""
    
    def __init__(self):
        """Initialize subscriber database operations."""
        self.db_manager = db_manager
    
    def add_subscriber(self, email: str, branch: Optional[str] = None, 
                      frequency: str = "weekly") -> Dict[str, Any]:
        """
        Add a new subscriber to the database.
        
        Args:
            email (str): Subscriber's email address
            branch (str, optional): Engineering branch (e.g., "CSE", "ECE")
            frequency (str): Email frequency ("daily", "weekly", "monthly")
        
        Returns:
            Dict[str, Any]: Result containing success status and data/error message
        """
        session = self.db_manager.get_session()
        try:
            # Validate frequency
            valid_frequencies = ["daily", "weekly", "monthly"]
            if frequency not in valid_frequencies:
                return {
                    "success": False,
                    "error": f"Invalid frequency. Must be one of: {', '.join(valid_frequencies)}"
                }
            
            # Normalize email
            email = email.strip().lower()
            
            # Create new subscriber
            subscriber = Subscriber(
                email=email,
                branch=branch.strip() if branch else None,
                frequency=frequency,
                status="active"
            )
            
            session.add(subscriber)
            session.commit()
            
            return {
                "success": True,
                "data": {
                    "id": subscriber.id,
                    "email": subscriber.email,
                    "branch": subscriber.branch,
                    "frequency": subscriber.frequency,
                    "status": subscriber.status,
                    "created_at": subscriber.created_at
                },
                "message": "Successfully subscribed!"
            }
            
        except IntegrityError:
            session.rollback()
            return {
                "success": False,
                "error": "Email already subscribed!"
            }
        except SQLAlchemyError as e:
            session.rollback()
            return {
                "success": False,
                "error": f"Database error: {str(e)}"
            }
        except Exception as e:
            session.rollback()
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
        finally:
            session.close()
    
    def get_active_subscribers(self) -> Dict[str, Any]:
        """
        Fetch all active subscribers.
        
        Returns:
            Dict[str, Any]: Result containing success status and subscribers data
        """
        session = self.db_manager.get_session()
        try:
            subscribers = session.query(Subscriber).filter(
                Subscriber.status == "active"
            ).order_by(Subscriber.created_at.desc()).all()
            
            data = [
                {
                    "id": sub.id,
                    "email": sub.email,
                    "branch": sub.branch,
                    "frequency": sub.frequency,
                    "status": sub.status,
                    "created_at": sub.created_at
                }
                for sub in subscribers
            ]
            
            return {
                "success": True,
                "data": data,
                "count": len(data)
            }
            
        except SQLAlchemyError as e:
            return {
                "success": False,
                "error": f"Failed to fetch subscribers: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
        finally:
            session.close()
    
    def get_all_subscribers(self) -> Dict[str, Any]:
        """
        Fetch all subscribers (active and unsubscribed).
        
        Returns:
            Dict[str, Any]: Result containing success status and subscribers data
        """
        session = self.db_manager.get_session()
        try:
            subscribers = session.query(Subscriber).order_by(
                Subscriber.created_at.desc()
            ).all()
            
            data = [
                {
                    "id": sub.id,
                    "email": sub.email,
                    "branch": sub.branch,
                    "frequency": sub.frequency,
                    "status": sub.status,
                    "created_at": sub.created_at
                }
                for sub in subscribers
            ]
            
            return {
                "success": True,
                "data": data,
                "count": len(data)
            }
            
        except SQLAlchemyError as e:
            return {
                "success": False,
                "error": f"Failed to fetch all subscribers: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
        finally:
            session.close()
    
    def unsubscribe_by_email(self, email: str) -> Dict[str, Any]:
        """
        Unsubscribe a user by email address.
        
        Args:
            email (str): Email address to unsubscribe
        
        Returns:
            Dict[str, Any]: Result containing success status and message
        """
        session = self.db_manager.get_session()
        try:
            # Normalize email
            email = email.strip().lower()
            
            # Find and update subscriber
            subscriber = session.query(Subscriber).filter(
                Subscriber.email == email,
                Subscriber.status == "active"
            ).first()
            
            if not subscriber:
                return {
                    "success": False,
                    "error": "Email not found or already unsubscribed"
                }
            
            subscriber.status = "unsubscribed"
            session.commit()
            
            return {
                "success": True,
                "data": {
                    "id": subscriber.id,
                    "email": subscriber.email,
                    "status": subscriber.status
                },
                "message": "Successfully unsubscribed"
            }
            
        except SQLAlchemyError as e:
            session.rollback()
            return {
                "success": False,
                "error": f"Database error: {str(e)}"
            }
        except Exception as e:
            session.rollback()
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
        finally:
            session.close()
    
    def update_subscriber_frequency(self, email: str, frequency: str) -> Dict[str, Any]:
        """
        Update a subscriber's email frequency.
        
        Args:
            email (str): Subscriber's email address
            frequency (str): New frequency ("daily", "weekly", "monthly")
        
        Returns:
            Dict[str, Any]: Result containing success status and data/error message
        """
        session = self.db_manager.get_session()
        try:
            # Validate frequency
            valid_frequencies = ["daily", "weekly", "monthly"]
            if frequency not in valid_frequencies:
                return {
                    "success": False,
                    "error": f"Invalid frequency. Must be one of: {', '.join(valid_frequencies)}"
                }
            
            # Normalize email
            email = email.strip().lower()
            
            # Find and update subscriber
            subscriber = session.query(Subscriber).filter(
                Subscriber.email == email,
                Subscriber.status == "active"
            ).first()
            
            if not subscriber:
                return {
                    "success": False,
                    "error": "Email not found or already unsubscribed"
                }
            
            subscriber.frequency = frequency
            session.commit()
            
            return {
                "success": True,
                "data": {
                    "id": subscriber.id,
                    "email": subscriber.email,
                    "frequency": subscriber.frequency
                },
                "message": f"Frequency updated to {frequency}"
            }
            
        except SQLAlchemyError as e:
            session.rollback()
            return {
                "success": False,
                "error": f"Database error: {str(e)}"
            }
        except Exception as e:
            session.rollback()
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
        finally:
            session.close()
    
    def get_subscriber_stats(self) -> Dict[str, Any]:
        """
        Get subscriber statistics.
        
        Returns:
            Dict[str, Any]: Statistics about subscribers
        """
        session = self.db_manager.get_session()
        try:
            # Get counts using database functions for efficiency
            result = session.execute(text("SELECT * FROM get_subscriber_stats()")).fetchone()
            
            if result:
                return {
                    "success": True,
                    "stats": {
                        "total_active": result[0],
                        "total_unsubscribed": result[1],
                        "total_all": result[2],
                        "frequency_breakdown": {
                            "daily": result[3],
                            "weekly": result[4],
                            "monthly": result[5]
                        }
                    }
                }
            else:
                # Fallback to manual counting if function doesn't exist
                active_count = session.query(Subscriber).filter(Subscriber.status == "active").count()
                total_count = session.query(Subscriber).count()
                daily_count = session.query(Subscriber).filter(
                    Subscriber.status == "active", Subscriber.frequency == "daily"
                ).count()
                weekly_count = session.query(Subscriber).filter(
                    Subscriber.status == "active", Subscriber.frequency == "weekly"
                ).count()
                monthly_count = session.query(Subscriber).filter(
                    Subscriber.status == "active", Subscriber.frequency == "monthly"
                ).count()
                
                return {
                    "success": True,
                    "stats": {
                        "total_active": active_count,
                        "total_unsubscribed": total_count - active_count,
                        "total_all": total_count,
                        "frequency_breakdown": {
                            "daily": daily_count,
                            "weekly": weekly_count,
                            "monthly": monthly_count
                        }
                    }
                }
            
        except SQLAlchemyError as e:
            return {
                "success": False,
                "error": f"Failed to get stats: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
        finally:
            session.close()


# Convenience functions for easy import
def get_db() -> SubscriberDB:
    """Get a database instance."""
    return SubscriberDB()

def subscribe_user(email: str, branch: Optional[str] = None, frequency: str = "weekly") -> Dict[str, Any]:
    """Subscribe a user - convenience function."""
    db = get_db()
    return db.add_subscriber(email, branch, frequency)

def unsubscribe_user(email: str) -> Dict[str, Any]:
    """Unsubscribe a user - convenience function."""
    db = get_db()
    return db.unsubscribe_by_email(email)

def get_active_users() -> Dict[str, Any]:
    """Get active subscribers - convenience function."""
    db = get_db()
    return db.get_active_subscribers()

# Database initialization function
def init_database():
    """Initialize database tables if they don't exist."""
    try:
        Base.metadata.create_all(bind=db_manager.engine)
        return True
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        return False
