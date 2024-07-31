import hmac
import streamlit as st
import PIL
import cv2
import numpy as np
import utility  # Ensure this module is available or replace with actual function

def check_password():
    """Returns `True` if the user has entered the correct password."""
    
    def login_form():
        """Form with widgets to collect user information."""
        st.header("AI Workforce Safety System")
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
    # Clear cache if necessary
    st.legacy_caching.clear_cache()

# Main app logic
if not check_password():
    st.stop()

# Show the main content if authenticated
st.set_page_config(
    page_title="AI Workforce Safety System",
    page_icon=":construction_worker:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("AI Workforce Safety System :construction_worker:")

st.sidebar.header("Type of PPE Detection")
source_radio = st.sidebar.radio("Select Source", ["IMAGE", "VIDEO", "WEBCAM"])

st.sidebar.header("Confidence")
conf_threshold = float(st.sidebar.slider("Select the Confidence Threshold", 10, 100, 20))/100

input = None
if source_radio == "IMAGE":
    st.sidebar.header("Upload")
    input = st.sidebar.file_uploader("Choose an image", type=("jpg", "png"))

    if input is not None:
        try:
            uploaded_image = PIL.Image.open(input)
            uploaded_image_cv = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
            visualized_image = utility.predict_image(uploaded_image_cv, conf_threshold=conf_threshold)
            st.image(visualized_image, channels="BGR")
        except Exception as e:
            st.error(f"Error processing image: {e}")
    else:
        st.image("assets/construct.jpg")
        st.write("Click on 'Browse Files' in the sidebar to run inference on an image.")

# Add logout button
if st.button("Logout"):
    logout()
    # Simply set the session state and let Streamlit's automatic rerun handle it
    st.session_state["password_correct"] = False
    st.legacy_caching.clear_cache()  # Clear cache to ensure a fresh start
