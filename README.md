# betterEngineer Newsletter

A Streamlit-based newsletter platform that delivers intelligent insights to build better engineers. Built with PostgreSQL database backend for robust subscriber management.

## 🚀 Features

- **Beautiful Landing Page**: Dark theme with animated background and interactive elements
- **Smart Subscription System**: PostgreSQL-powered with duplicate prevention and validation
- **Admin Dashboard**: Complete subscriber management with analytics and export capabilities
- **Multi-frequency Support**: Daily, weekly, or monthly newsletter options
- **Engineering Branch Tracking**: Optional field for personalized content
- **Production Ready**: Connection pooling, error handling, and security features

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Icons**: Feather Icons
- **Hosting**: Compatible with Railway, Render, Neon, or any PostgreSQL provider

## 📦 Quick Setup

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd better-engineer-newsletter
uv sync  # or pip install -r requirements.txt
```

### 2. Set Up Database

Choose one of these PostgreSQL hosting options:
- **Railway.app** (recommended for ease of use)
- **Render.com** (good free tier)
- **Neon.tech** (serverless PostgreSQL)
- **Local PostgreSQL** (for development)

See detailed setup instructions in `SUPABASE_SETUP.md`.

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Initialize Database

```bash
python test_db.py  # Test connection and setup
```

### 5. Run Application

```bash
streamlit run Home.py
```

## 🗄️ Database Schema

```sql
CREATE TABLE subscribers (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    branch TEXT NULL,
    frequency TEXT NOT NULL DEFAULT 'weekly',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Environment Variables

Required in `.env` file:

```env
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_username
DB_PASS=your_password
DB_PORT=5432
```

## 📊 Admin Dashboard

Access the admin dashboard at `/Admin` with:
- **Default Password**: `admin123` (change in production!)
- **Features**: 
  - Subscriber overview and statistics
  - Export data to CSV
  - Manual unsubscribe functionality
  - Real-time analytics charts

## 🏗️ Project Structure

```
better-engineer-newsletter/
├── Home.py                 # Main landing page
├── db.py                   # Database layer with SQLAlchemy
├── database_schema.sql     # PostgreSQL table definitions
├── test_db.py             # Database connection test script
├── .env.example           # Environment variables template
├── pages/
│   ├── 1_About.py         # About page
│   └── 2_Admin.py         # Admin dashboard
├── feather/               # Icon assets
└── pyproject.toml         # Python dependencies
```

## 🔐 Security Features

- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Connection Pooling**: Optimized database connections
- **Input Validation**: Email format and frequency validation
- **Duplicate Prevention**: Unique email constraints
- **Environment Variables**: Secure credential management

## 🚀 Deployment

### Railway.app
1. Connect your GitHub repository
2. Add environment variables in Railway dashboard
3. Deploy automatically

### Render.com
1. Create new Web Service from GitHub
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run Home.py --server.port $PORT`
4. Add environment variables

### Streamlit Cloud
1. Connect repository to Streamlit Cloud
2. Add secrets in dashboard (equivalent to .env)
3. Deploy with one click

## 📈 Performance

- **Connection Pooling**: 10 base connections, 20 max overflow
- **Query Optimization**: Indexed fields for fast lookups
- **Efficient Statistics**: Database functions for analytics
- **Memory Management**: Proper session handling

## 🧪 Testing

Run the database test suite:

```bash
python test_db.py
```

This will test:
- Database connection
- Table creation
- Subscriber operations
- Statistics generation
- Error handling

## 📝 API Usage

```python
from db import subscribe_user, unsubscribe_user, get_active_users

# Subscribe a user
result = subscribe_user("user@example.com", "CSE", "weekly")

# Unsubscribe a user
result = unsubscribe_user("user@example.com")

# Get all active subscribers
users = get_active_users()
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python test_db.py`
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- Check `SUPABASE_SETUP.md` for detailed setup instructions
- Run `python test_db.py` to diagnose database issues
- Review logs in your hosting platform dashboard

---

**Built with ❤️ for better engineers everywhere**