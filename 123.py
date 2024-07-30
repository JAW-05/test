import hmac
import streamlit as st

def check_password():
    """Returns `True` if the user has entered the correct password."""
    
    def login_form():
        """Form with widgets to collect user information."""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            submitted = st.form_submit_button("Log in")
            if submitted:
                password_entered()

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        username = st.session_state.get("username")
        password = st.session_state.get("password")
        
        if username and password:
            stored_password = st.secrets["passwords"].get(username)
            if stored_password and hmac.compare_digest(password, stored_password):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the password.
                del st.session_state["username"]
            else:
                st.session_state["password_correct"] = False
        else:
            st.session_state["password_correct"] = False

    # Initialize session state if not already done
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state["password_correct"]:
        return True

    # Show inputs for username + password.
    login_form()
    if not st.session_state["password_correct"]:
        st.error("😕 User not known or password incorrect")
    return False


def logout():
    """Resets the session state to log out the user."""
    st.session_state["password_correct"] = False
    if "username" in st.session_state:
        del st.session_state["username"]
    if "password" in st.session_state:
        del st.session_state["password"]  # Remove the password from session state.

# Main app logic
if not check_password():
    st.stop()

# Show the main content if authenticated
st.write("Here goes your normal Streamlit app...")
st.button("Click me")

# Add logout button
if st.button("Logout"):
    logout()
    # Simply set the session state and let Streamlit's automatic rerun handle it
    st.session_state["password_correct"] = False
    st.experimental_rerun()
