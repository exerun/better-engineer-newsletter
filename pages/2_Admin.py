import streamlit as st
import pandas as pd
from db import get_db

st.set_page_config(
    page_title="Admin Dashboard - betterEngineer",
    page_icon="⚙️",
    layout="wide",
)

# Add simple authentication (for demo purposes)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Admin Login")
    
    with st.form("login_form"):
        password = st.text_input("Admin Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            # Simple password check (in production, use proper authentication)
            if password == "admin123":  # Change this to a secure password
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
    
    st.info("💡 Default password: admin123 (change this in production!)")
    st.stop()

# Logout button
if st.button("🚪 Logout", type="secondary"):
    st.session_state.authenticated = False
    st.rerun()

st.title("⚙️ Admin Dashboard")
st.markdown("---")

# Initialize database
try:
    db = get_db()
except Exception as e:
    st.error(f"Database connection failed: {str(e)}")
    st.info("Make sure your Supabase credentials are properly configured in the .env file.")
    st.stop()

# Sidebar for navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Select Page", [
    "📈 Overview",
    "👥 Subscribers",
    "📧 Unsubscribe",
    "📊 Statistics"
])

if page == "📈 Overview":
    st.header("📈 Overview")
    
    # Get statistics
    stats_result = db.get_subscriber_stats()
    
    if stats_result["success"]:
        stats = stats_result["stats"]
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Active", stats["total_active"])
        
        with col2:
            st.metric("Total Unsubscribed", stats["total_unsubscribed"])
        
        with col3:
            st.metric("Total All Time", stats["total_all"])
        
        with col4:
            conversion_rate = (stats["total_active"] / max(stats["total_all"], 1)) * 100
            st.metric("Retention Rate", f"{conversion_rate:.1f}%")
        
        # Frequency breakdown
        st.subheader("📅 Subscription Frequency Breakdown")
        freq_data = stats["frequency_breakdown"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Daily", freq_data["daily"])
        with col2:
            st.metric("Weekly", freq_data["weekly"])
        with col3:
            st.metric("Monthly", freq_data["monthly"])
            
        # Chart for frequency breakdown
        if any(freq_data.values()):
            chart_data = pd.DataFrame({
                'Frequency': list(freq_data.keys()),
                'Count': list(freq_data.values())
            })
            st.bar_chart(chart_data.set_index('Frequency'))
    
    else:
        st.error(f"Failed to load statistics: {stats_result['error']}")

elif page == "👥 Subscribers":
    st.header("👥 Subscriber Management")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Unsubscribed"])
    with col2:
        frequency_filter = st.selectbox("Filter by Frequency", ["All", "daily", "weekly", "monthly"])
    
    # Get subscribers
    if status_filter == "Active":
        result = db.get_active_subscribers()
    else:
        result = db.get_all_subscribers()
    
    if result["success"]:
        subscribers = result["data"]
        
        if subscribers:
            # Convert to DataFrame for better display
            df = pd.DataFrame(subscribers)
            
            # Apply filters
            if status_filter != "All" and status_filter != "Active":
                df = df[df['status'] == status_filter.lower()]
            
            if frequency_filter != "All":
                df = df[df['frequency'] == frequency_filter]
            
            # Format the dataframe
            if not df.empty:
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                
                # Display count
                st.write(f"**Total: {len(df)} subscribers**")
                
                # Display table with edit options
                st.dataframe(
                    df[['email', 'branch', 'frequency', 'status', 'created_at']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Export option
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"subscribers_{status_filter.lower()}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No subscribers match the selected filters.")
        else:
            st.info("No subscribers found.")
    else:
        st.error(f"Failed to load subscribers: {result['error']}")

elif page == "📧 Unsubscribe":
    st.header("📧 Unsubscribe Management")
    
    with st.form("unsubscribe_form"):
        st.write("Manually unsubscribe a user by email:")
        email = st.text_input("Email Address")
        unsubscribe_button = st.form_submit_button("Unsubscribe")
        
        if unsubscribe_button and email:
            result = db.unsubscribe_by_email(email)
            
            if result["success"]:
                st.success(f"✅ {result['message']}")
            else:
                st.error(f"❌ {result['error']}")

elif page == "📊 Statistics":
    st.header("📊 Detailed Statistics")
    
    # Get all subscribers for analysis
    result = db.get_all_subscribers()
    
    if result["success"] and result["data"]:
        df = pd.DataFrame(result["data"])
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Daily signups chart
        st.subheader("📈 Daily Signups")
        daily_signups = df.groupby(df['created_at'].dt.date).size().reset_index()
        daily_signups.columns = ['Date', 'Signups']
        
        if not daily_signups.empty:
            st.line_chart(daily_signups.set_index('Date'))
        
        # Branch distribution
        st.subheader("🎓 Engineering Branch Distribution")
        branch_counts = df['branch'].value_counts().fillna('Not Specified')
        
        if not branch_counts.empty:
            st.bar_chart(branch_counts)
        
        # Status distribution
        st.subheader("📊 Status Distribution")
        status_counts = df['status'].value_counts()
        st.bar_chart(status_counts)
        
        # Recent activity
        st.subheader("🕒 Recent Subscriptions")
        recent = df.sort_values('created_at', ascending=False).head(10)
        st.dataframe(
            recent[['email', 'branch', 'frequency', 'status', 'created_at']],
            use_container_width=True,
            hide_index=True
        )
    
    else:
        st.info("No data available for analysis.")

# Footer
st.markdown("---")
st.markdown("💡 **Note**: This is a demo admin interface. In production, implement proper authentication and authorization.")
