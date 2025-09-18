# PostgreSQL Database Setup Guide for betterEngineer

This guide covers setting up a PostgreSQL database for betterEngineer using free hosting platforms like Railway, Render, or Neon.

## 1. Choose a PostgreSQL Hosting Provider

### Option A: Railway.app (Recommended)
1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click "New Project" → "Provision PostgreSQL"
3. Wait for deployment (2-3 minutes)
4. Go to your database service → "Connect" tab
5. Copy the connection details

### Option B: Render.com
1. Go to [render.com](https://render.com) and create an account
2. Click "New +" → "PostgreSQL"
3. Choose a name and region
4. Select the free plan
5. Click "Create Database"
6. Copy the connection details from the dashboard

### Option C: Neon.tech
1. Go to [neon.tech](https://neon.tech) and sign up
2. Create a new project
3. Choose a region and PostgreSQL version
4. Copy the connection string from the dashboard

### Option D: Local Development
1. Install PostgreSQL locally
2. Create a database named `betterengineer`
3. Use default settings (host: localhost, port: 5432)

## 2. Set Up the Database Schema

### Method 1: Using psql command line
```bash
# Connect to your database
psql "postgresql://username:password@host:port/database"

# Copy and paste the contents of database_schema.sql
\i database_schema.sql
```

### Method 2: Using a GUI tool
1. Use pgAdmin, DBeaver, or TablePlus
2. Connect to your database
3. Open `database_schema.sql` and execute it

### Method 3: Using Python script
```python
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Read the schema file
with open('database_schema.sql', 'r') as file:
    schema_sql = file.read()

# Connect and execute
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    port=os.getenv("DB_PORT", 5432)
)

cursor = conn.cursor()
cursor.execute(schema_sql)
conn.commit()
conn.close()
```

## 3. Configure Environment Variables

1. Copy the environment template:

```bash
cp .env.example .env
```

2. Edit `.env` with your database credentials:

```env
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_username
DB_PASS=your_password
DB_PORT=5432
```

### Example configurations:

**Railway:**
```env
DB_HOST=containers-us-west-xyz.railway.app
DB_NAME=railway
DB_USER=postgres
DB_PASS=your_railway_password
DB_PORT=5432
```

**Render:**
```env
DB_HOST=dpg-xyz-a.oregon-postgres.render.com
DB_NAME=your_database_name
DB_USER=your_username
DB_PASS=your_render_password
DB_PORT=5432
```

**Neon:**
```env
DB_HOST=ep-xyz.us-east-1.aws.neon.tech
DB_NAME=neondb
DB_USER=your_username
DB_PASS=your_neon_password
DB_PORT=5432
```

## 4. Install Dependencies

```bash
# Install Python dependencies
uv sync

# Or if using pip:
pip install sqlalchemy psycopg2-binary python-dotenv streamlit
```

## 5. Test the Database Connection

1. Run the Streamlit app:

```bash
streamlit run Home.py
```

2. Try subscribing with a test email
3. Check your database to see if the subscriber was added

### Database Testing Script

Create `test_db.py`:
```python
from db import init_database, subscribe_user, get_active_users

# Initialize database
if init_database():
    print("✅ Database initialized successfully")
    
    # Test subscription
    result = subscribe_user("test@example.com", "CSE", "weekly")
    if result["success"]:
        print("✅ Subscription test passed")
    else:
        print(f"❌ Subscription failed: {result['error']}")
    
    # Test retrieval
    users = get_active_users()
    if users["success"]:
        print(f"✅ Found {users['count']} active subscribers")
    else:
        print(f"❌ Failed to get users: {users['error']}")
else:
    print("❌ Database initialization failed")
```

Run it:
```bash
python test_db.py
```

## 6. Database Schema Overview

The `subscribers` table includes:

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key (auto-increment) |
| `email` | TEXT | Unique email address |
| `branch` | TEXT | Engineering branch (optional) |
| `frequency` | TEXT | Email frequency (daily/weekly/monthly) |
| `status` | TEXT | Subscription status (active/unsubscribed) |
| `created_at` | TIMESTAMP | Subscription date |

## 7. Production Features

### Connection Pooling
- Uses SQLAlchemy's QueuePool for efficient connection management
- Pool size: 10 connections
- Max overflow: 20 connections
- Connection recycling every hour

### Error Handling
- Proper transaction rollback on errors
- Detailed error messages
- Graceful handling of duplicate emails

### Security
- SQL injection prevention via SQLAlchemy ORM
- Environment variable configuration
- Connection validation with pool_pre_ping

## 8. Available Database Operations

The `db.py` module provides these functions:

```python
from db import subscribe_user, unsubscribe_user, get_active_users, get_db

# Subscribe a user
result = subscribe_user("user@example.com", "CSE", "weekly")

# Unsubscribe a user
result = unsubscribe_user("user@example.com")

# Get active subscribers
users = get_active_users()

# Get database instance for advanced operations
db = get_db()
stats = db.get_subscriber_stats()
```

## 9. Admin Dashboard

The admin dashboard (`pages/2_Admin.py`) provides:
- Subscriber overview and statistics
- Subscriber management with filtering
- Manual unsubscribe functionality
- Data export capabilities
- Real-time analytics

Default admin password: `admin123` (change in production!)

## 10. Deployment Considerations

### Environment Variables
Make sure to set these in your deployment platform:
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASS`
- `DB_PORT`

### Database Backups
- Railway: Automatic backups on paid plans
- Render: Manual backups via dashboard
- Neon: Automatic backups included

### Monitoring
- Monitor database connections in your hosting dashboard
- Set up alerts for database errors
- Track subscription metrics

## Troubleshooting

### Common Issues:

1. **"Missing required database environment variables"**
   - Check that all DB_* variables are set in .env
   - Verify variable names match exactly

2. **"Database connection failed"**
   - Verify credentials are correct
   - Check if database server is running
   - Ensure your IP is whitelisted (if required)

3. **"Import psycopg2 could not be resolved"**
   - Run `pip install psycopg2-binary`
   - Or use `uv sync` to install all dependencies

4. **"relation 'subscribers' does not exist"**
   - Run the database schema script
   - Check if you're connecting to the correct database

5. **Connection timeout issues**
   - Check your internet connection
   - Verify the database host and port
   - Try connecting with a different tool first

### Performance Tips:

1. **Index Usage**: The schema includes indexes on email, status, and created_at
2. **Connection Pooling**: Configured for optimal performance
3. **Query Optimization**: Use the provided functions for best performance

### Getting Help:

- Check PostgreSQL documentation: [postgresql.org/docs](https://postgresql.org/docs)
- Review your hosting provider's documentation
- Check the database logs in your hosting dashboard
