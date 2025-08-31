import streamlit as st

st.set_page_config(
    page_title="About betterEngineer",
    page_icon="🧠",
    layout="centered",
)

st.title("About Us")
st.markdown("---")

st.markdown("""
### Our Mission
We believe that continuous learning is the cornerstone of a great engineering career. 
Our mission is to cut through the noise and deliver the most essential, cross-disciplinary knowledge 
that every engineer needs, from foundational concepts to practical life skills.

### How It Works
Our platform uses a team of specialized AI agents to perform the heavy lifting:
- **Scouting Agents** scan hundreds of sources for the latest tech news and deep-dive topics.
- **Writing Agents** summarize and simplify complex information into an engaging, 3-minute read.
- **Publishing Agents** assemble and deliver the final newsletter to your inbox every week.

This AI-powered workflow ensures you get high-quality, relevant content without the fluff, allowing you to **Be a betterEngineer.**
""")
