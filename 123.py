import streamlit as st
import hmac
import PIL
import cv2
import numpy
import aiutils
import io

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

# Main app logic
if not check_password():
    st.stop()

def play_video(video_source):
    camera = cv2.VideoCapture(video_source)

    st_frame = st.empty()
    while(camera.isOpened()):
        ret, frame = camera.read()

        if ret:
            visualized_frame = aiutils.predict_image(frame, conf_threshold)
            st_frame.image(visualized_frame, channels = "BGR")

        else:
            camera.release()
            break

st.set_page_config(
    page_title="AI Workspace Safety System",
    page_icon="👷",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("👷 AI Workspace Safety System")

st.sidebar.header("Type")
source_radio = st.sidebar.radio("Select Type", ["Detection PPE(Personal Protective Equipment)"])

st.sidebar.header("Select Object to Recognition")
source_bt = st.sidebar.button("Helmets")
source_bt = st.sidebar.button("Glasses")
source_bt = st.sidebar.button("Gloves")
source_bt = st.sidebar.button("Vests")
source_bt = st.sidebar.button("Boots")

st.sidebar.header("Confidence")
conf_threshold = float(st.sidebar.slider("Select the Confidence Threshold", 10, 100, 20))/100

if source_radio == "WEBCAM":
    play_video(0)

if st.button("Logout"):
    logout()
    # Simply set the session state and let Streamlit's automatic rerun handle it
    st.session_state["password_correct"] = False
    st.experimental_rerun()
