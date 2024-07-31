import streamlit as st

def check_password():
    """Returns `True` if the user has entered the correct password."""
    
    def login_form():
        """Form with widgets to collect user information."""
        st.header("Login to AI Workforce Safety System")
        with st.form("Credentials"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")
            if submitted:
                if authenticate(username, password):
                    st.session_state["password_correct"] = True
                    st.session_state["username"] = username
                else:
                    st.session_state["password_correct"] = False

    def authenticate(username, password):
        """Authenticates user by checking the password."""
        stored_password = st.secrets["passwords"].get(username)
        return stored_password == password

    # Initialize session state if not already done
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state["password_correct"]:
        return True

    # Show inputs for username + password.
    login_form()
    if not st.session_state["password_correct"]:
        st.error("😕 Username or password is incorrect")
    return False

def logout():
    """Resets the session state to log out the user."""
    st.session_state["password_correct"] = False
    if "username" in st.session_state:
        del st.session_state["username"]

# Main app logic
if not check_password():
    st.stop()

# Show the main content if authenticated
st.set_page_config(
    page_title="AI Workforce Safety System",
    page_icon=":construction_worker:",
    layout="centered"
)

st.title("Welcome to the AI Workforce Safety System :construction_worker:")

st.write("You have successfully logged in!")

# Add logout button
if st.button("Logout"):
    logout()
    st.experimental_rerun()
