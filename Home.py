import streamlit as st
import time

# Page configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="betterEngineer — Home",
    page_icon="🧠",
    layout="centered",
)

# --- Updated CSS with a RELIABLE, embedded and animated doodle background ---
st.markdown(
    """
    <style>
    @keyframes moveBackground {
      0% { background-position: 0 0; }
      100% { background-position: 40px 40px; } /* Match the size of the pattern */
    }

    .stApp {
        background-color: #1c1c24;
        /* Using an embedded SVG for reliability. This is a subtle "tic-tac-toe" pattern. */
        background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.05' fill-rule='evenodd'%3E%3Cpath d='M0 20L20 0H10L0 10M20 20V10L10 20'/%3E%3C/g%3E%3C/svg%3E");
        background-repeat: repeat;
        animation: moveBackground 4s linear infinite; /* Slowed down animation */
    }

    /* Style for the feature columns */
    .feature-col {
        border: 1px solid #2a2a32;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        background-color: #1c1c24e0; /* Semi-transparent background to make text readable */
    }
    .feature-col:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .feature-col img {
        width: 50px;
        height: 50px;
        margin-bottom: 15px;
        background-color: #1c1c24e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title('Be a :blue["betterEngineer"]')
st.subheader("Intelligent insights that build better engineers.")
st.markdown("---") # Adds a horizontal line

# --- Updated section with styled columns and icons ---
st.markdown("#### What you'll get every week:")
col1, col2, col3 = st.columns(3)

# Use local feather-icons (light mode: black stroke)
def feather_icon(icon_name):
    icon_path = f"node_modules/feather-icons/dist/icons/{icon_name}.svg"
    try:
        with open(icon_path, "r") as f:
            svg = f.read()
        # Patch SVG: set width/height to 48, force white stroke, and add style for display
        svg = svg.replace('<svg ', '<svg style="width:48px;height:48px;display:block;margin:0 auto;" stroke="#fff" ')
        return f'<span style="display:inline-block;vertical-align:middle;">{svg}</span>'
    except Exception:
        return ""

with col1:
    with st.container():
        st.markdown(f"""
        <div class="feature-col">
            {feather_icon('pen-tool')}
            <h5>Tech News</h5>
            <p>The top 2-3 most important headlines in the tech and engineering world, summarized for you.</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown(f"""
        <div class="feature-col">
            {feather_icon('cpu')}
            <h5>Core Concepts</h5>
            <p>A deep dive into one essential engineering topic, from CS fundamentals to universal principles.</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown(f"""
        <div class="feature-col">
            {feather_icon('settings')}
            <h5>Life Skills</h5>
            <p>Practical knowledge that isn't taught in school, from understanding taxes to personal finance.</p>
        </div>
        """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True) # Add some space

# --- Added a new "Sample Snippet" section ---
with st.expander("See a Sample Snippet"):
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px;">
        {feather_icon('cpu')}
        <span style="font-size: 1.1em; font-weight: 600;">Core Concept: What is an API?</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    Imagine you're at a restaurant. You don't go into the kitchen to cook your food; you give your order to a waiter. The waiter (the **API**) takes your request to the kitchen (**the system**), gets the food (**the data**), and brings it back to you.

    An **Application Programming Interface (API)** is that waiter. It's a set of rules that lets different software applications talk to each other, requesting and exchanging information without needing to know how the other system works internally. It's the backbone of the modern web!
    """)


st.markdown("---")

# --- Subscription Form (Unchanged) ---
with st.form(key="subscription_form"):
    st.markdown("##### Ready to level up? Subscribe for your weekly brief.")
    email = st.text_input(
        "Enter your email address",
        placeholder="you@domain.com",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Subscribe Now")

    if submitted:
        if email and "@" in email and "." in email:
            with st.spinner("Subscribing..."):
                # TODO: Add database logic here
                time.sleep(2)
            st.success("✅ Success! You're on the list. Check your inbox.")
        else:
            st.error("⚠️ Please enter a valid email address.")

# --- Added a simple footer ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2024 betterEngineer. All rights reserved.</div>", unsafe_allow_html=True)

