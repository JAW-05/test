import hmac
import streamlit as st

def check_password():
    """Returns `True` if the user has a correct password."""

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
        if st.session_state["username"] in st.secrets["passwords"] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets["passwords"][st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 User not known or password incorrect")
    return False


def logout():
    """Resets the session state to log out the user."""
    if "password_correct" in st.session_state:
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
    # Optionally use a placeholder to trigger an update in the session state
    st.session_state["password_correct"] = False
    st.experimental_rerun()  # Rerun the app to show the login screen again.
