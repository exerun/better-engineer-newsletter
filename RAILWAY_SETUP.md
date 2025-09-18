# Railway.app Production Setup for betterEngineer

## 🚂 Quick Railway Setup (5 minutes)

### 1. Create Railway Database
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"**
4. Select **"Provision PostgreSQL"**
5. Wait for deployment (2-3 minutes)

### 2. Get Your Database Credentials
1. Click on your **PostgreSQL service**
2. Go to **"Connect"** tab
3. Copy these values:

```
Host: containers-us-west-xyz.railway.app
Port: 5432
Database: railway
Username: postgres
Password: [long random string]
```

### 3. Update Your .env File
Replace the placeholders in your `.env` file:

```env
DB_HOST=containers-us-west-xyz.railway.app  # Your Railway host
DB_NAME=railway                             # Usually 'railway'
DB_USER=postgres                            # Usually 'postgres'
DB_PASS=ABC123xyz789                        # Your Railway password
DB_PORT=5432                               # Standard port
```

### 4. Set Up Database Schema
Run this command to create the tables:

```bash
uv run python setup_railway.py
```

### 5. Test Your Setup
```bash
uv run python test_db.py
```

### 6. Launch Your App
```bash
uv run streamlit run Home.py
```

## 🌐 Deploy to Railway (Optional)

### Option A: Deploy Frontend to Railway
1. In Railway dashboard, click **"New Service"**
2. Connect your GitHub repository
3. Railway will auto-detect it's a Python app
4. Set environment variables in Railway:
   - `DB_HOST` = (your database host)
   - `DB_NAME` = railway
   - `DB_USER` = postgres
   - `DB_PASS` = (your database password)
   - `DB_PORT` = 5432

### Option B: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repo
3. Add secrets (equivalent to .env):
   ```
   DB_HOST = "your-railway-host"
   DB_NAME = "railway"
   DB_USER = "postgres"
   DB_PASS = "your-password"
   DB_PORT = "5432"
   ```

## 💰 Railway Pricing for Production

### Starter Plan ($5/month credit)
- **Database**: ~$3-4/month for small apps
- **Storage**: 1GB included
- **Compute**: Always-on
- **Perfect for**: Newsletter with <10k subscribers

### Usage Estimates for betterEngineer:
- **Database**: $2-3/month (small usage)
- **Bandwidth**: Minimal (form submissions)
- **Storage**: <100MB for thousands of subscribers
- **Total**: ~$3-5/month

## 🔧 Railway CLI (Optional)

Install Railway CLI for easier management:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Connect to your database directly
railway connect
```

## 📊 Monitoring Your Production Database

### Railway Dashboard Features:
- **Metrics**: View database usage and performance
- **Logs**: Monitor connection and query logs
- **Backups**: Automatic backups (paid plans)
- **Scaling**: Easy vertical scaling

### Key Metrics to Watch:
- **Active Connections**: Should stay under 100
- **Storage Usage**: Monitor growth
- **Query Performance**: Check slow queries
- **Error Rates**: Monitor failed connections

## 🔐 Production Security Checklist

- ✅ SSL connection enforced (Railway default)
- ✅ Environment variables (not hardcoded)
- ✅ Connection pooling (SQLAlchemy handles this)
- ✅ Input validation (implemented in db.py)
- ✅ Unique constraints (prevents duplicate emails)

## 🚨 Troubleshooting

### Common Issues:

1. **"Connection refused"**
   - Check if Railway database is running
   - Verify host and port are correct

2. **"Authentication failed"**
   - Double-check username and password
   - Ensure no extra spaces in credentials

3. **"SSL required"**
   - Railway requires SSL connections
   - Our setup includes `sslmode='require'`

4. **"Too many connections"**
   - Railway has connection limits
   - Our connection pooling should handle this

### Getting Help:
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Database logs in Railway dashboard

## 📈 Scaling Your Newsletter

As your newsletter grows:

### At 1,000 subscribers:
- Current setup handles easily
- ~$3-5/month Railway costs

### At 10,000 subscribers:
- May need to optimize queries
- Consider upgrading Railway plan
- ~$10-15/month estimated

### At 100,000+ subscribers:
- Consider dedicated database hosting
- Implement email service (SendGrid, etc.)
- Add CDN for assets

Your Railway PostgreSQL setup is production-ready and will scale with your newsletter growth! 🚀
