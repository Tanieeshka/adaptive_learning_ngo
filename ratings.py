import streamlit as st

# Page configuration
st.set_page_config(page_title="Peer Learning Matchmaking System", layout="centered")

st.title("Peer Learning Matchmaking System")
st.subheader("Rate Session")

# Mentor name (can be dynamic)
mentor_name = "Mentor: Rahul Sharma"
st.write(mentor_name)

st.write("### Please rate your mentor")

# Star rating options
rating = st.radio(
    label="Rating",
    options=[1, 2, 3, 4, 5],
    format_func=lambda x: "⭐" * x,
    horizontal=True
)

# Submit button
if st.button("Submit Rating"):
    # Backend logic placeholder
    # Example: save_rating(mentor_id, rating)
    
    st.success(f"Thank you! You rated this mentor {rating} ⭐")
