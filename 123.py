import hmac
import streamlit as st


def check_password():
    """Returns `True` if the user has entered the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        username = st.session_state.get("username")
        password = st.session_state.get("password")
        
        if username and password:
            stored_password = st.secrets["passwords"].get(username)
            if stored_password and hmac.compare_digest(password, stored_password):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the password.
            else:
                st.session_state["password_correct"] = False
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for username and password.
    if "username" not in st.session_state:
        st.session_state["username"] = st.text_input("Username", key="username")
    
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password incorrect")

    return False


def logout():
    """Resets the session state to log out the user."""
    st.session_state["password_correct"] = False
    if "username" in st.session_state:
        del st.session_state["username"]
    if "password" in st.session_state:
        del st.session_state["password"]  # Remove the password from session state.


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here
st.write("Welcome to AI Workforce Safety System!")

# Add logout button
if st.button("Logout"):
    logout()
    st.experimental_rerun()  # Rerun the app to show the login screen again.
