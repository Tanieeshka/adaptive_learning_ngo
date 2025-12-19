import streamlit as st

def calculate_points(rating):
    return rating * 10   # simple logic: 5⭐ = 50 points

st.set_page_config(page_title="Star Rating", page_icon="⭐")

# ---- Custom CSS for colors ----
st.markdown(
    """
    <style>
    /* Style all star buttons */
    div.stButton > button.star-btn {
        background-color: #2563eb;
        color: white;
        border-radius: 999px;
        border: none;
        padding: 0.4rem 0.8rem;
        margin: 0 0.1rem;
    }
    div.stButton > button.star-btn:hover {
        background-color: #106EBE;
    }

    /* Style submit button */
    div.stButton > button.submit-btn {
        background-color: #106EBE;
        color: white;
        border-radius: 999px;
        border: none;
        padding: 0.5rem 1.2rem;
        margin-top: 0.5rem;
    }
    div.stButton > button.submit-btn:hover {
        background-color: #2563eb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Rate your mentoring experience.")

# Initialize rating in session state
if "rating" not in st.session_state:
    st.session_state.rating = 0

st.write("Click on the stars to rate (1–5):")

cols = st.columns(5)

# Create 5 star buttons
for i in range(5):
    star_symbol = "⭐" if i < st.session_state.rating else "☆"
    with cols[i]:
        # Inject a small HTML wrapper so CSS can target this button as 'star-btn'
        st.markdown("<div class='star-btn-wrapper'></div>", unsafe_allow_html=True)
        if st.button(star_symbol, key=f"star_{i+1}"):
            st.session_state.rating = i + 1

# Submit button
st.markdown("<div class='submit-btn-wrapper'></div>", unsafe_allow_html=True)
submitted = st.button("Submit rating", key="submit")

if submitted:
    if st.session_state.rating > 0:
        points = calculate_points(st.session_state.rating)
        st.success(
            f"Thank you! Rating: {st.session_state.rating}/5 ⭐ | Mentor earned {points} points 🎯"
        )
    else:
        st.warning("Please select a rating before submitting.")

