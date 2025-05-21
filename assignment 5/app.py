import streamlit as st
import uuid
from datetime import datetime
from encryption import EncryptionManager
from storage import StorageManager

# Initialize session state
if 'encryption_manager' not in st.session_state:
    st.session_state.encryption_manager = EncryptionManager()
if 'storage_manager' not in st.session_state:
    st.session_state.storage_manager = StorageManager()
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_data_id' not in st.session_state:
    st.session_state.current_data_id = None

def login_page():
    st.title("🔑 Login Required")
    st.warning("Please authenticate to continue.")
    
    master_password = st.text_input("Enter Master Password", type="password")
    if st.button("Login"):
        # In a real application, this should be properly hashed and stored securely
        if master_password == "admin123":  # Demo password
            st.session_state.authenticated = True
            st.session_state.storage_manager.reset_failed_attempts(st.session_state.current_data_id)
            st.success("Authentication successful!")
            st.experimental_rerun()
        else:
            st.error("Incorrect password!")

def home_page():
    st.title("🔒 Secure Data Encryption System")
    st.write("Welcome to the Secure Data System! Use this application to store and retrieve your sensitive data securely.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Store New Data")
        st.write("Encrypt and store your sensitive data with a unique passkey.")
        if st.button("Go to Store Data"):
            st.session_state.page = "store"
            st.experimental_rerun()
    
    with col2:
        st.subheader("🔍 Retrieve Data")
        st.write("Retrieve your stored data using your passkey.")
        if st.button("Go to Retrieve Data"):
            st.session_state.page = "retrieve"
            st.experimental_rerun()

def store_data_page():
    st.title("📝 Store New Data")
    
    with st.form("store_data_form"):
        user_data = st.text_area("Enter Data to Encrypt:", height=150)
        passkey = st.text_input("Enter Passkey:", type="password")
        confirm_passkey = st.text_input("Confirm Passkey:", type="password")
        
        submitted = st.form_submit_button("Encrypt & Store")
        
        if submitted:
            if not user_data or not passkey or not confirm_passkey:
                st.error("All fields are required!")
            elif passkey != confirm_passkey:
                st.error("Passkeys do not match!")
            else:
                try:
                    # Generate unique ID for the data
                    data_id = str(uuid.uuid4())
                    
                    # Encrypt data and hash passkey
                    encrypted_text = st.session_state.encryption_manager.encrypt_data(user_data)
                    hashed_passkey = st.session_state.encryption_manager.hash_passkey(passkey)
                    
                    # Store the data
                    st.session_state.storage_manager.store_data(data_id, encrypted_text, hashed_passkey)
                    
                    st.success("✅ Data stored successfully!")
                    st.info(f"Your Data ID: {data_id}\n\nPlease save this ID to retrieve your data later!")
                    
                    # Clear the form
                    st.session_state.page = "home"
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error storing data: {str(e)}")

def retrieve_data_page():
    st.title("🔍 Retrieve Data")
    
    with st.form("retrieve_data_form"):
        data_id = st.text_input("Enter Data ID:")
        passkey = st.text_input("Enter Passkey:", type="password")
        
        submitted = st.form_submit_button("Retrieve Data")
        
        if submitted:
            if not data_id or not passkey:
                st.error("Both Data ID and Passkey are required!")
            else:
                # Check for lockout
                if st.session_state.storage_manager.is_locked_out(data_id):
                    remaining_time = st.session_state.storage_manager.get_remaining_lockout_time(data_id)
                    st.error(f"🔒 This data is locked out. Please try again in {int(remaining_time.total_seconds() / 60)} minutes.")
                    st.session_state.authenticated = False
                    st.session_state.current_data_id = data_id
                    st.session_state.page = "login"
                    st.experimental_rerun()
                
                # Get stored data
                stored_data = st.session_state.storage_manager.get_data(data_id)
                if not stored_data:
                    st.error("Data ID not found!")
                else:
                    # Verify passkey and decrypt
                    if st.session_state.encryption_manager.verify_passkey(stored_data["passkey"], passkey):
                        try:
                            decrypted_text = st.session_state.encryption_manager.decrypt_data(stored_data["encrypted_text"])
                            st.success("✅ Data retrieved successfully!")
                            st.text_area("Decrypted Data:", decrypted_text, height=150)
                            st.session_state.storage_manager.reset_failed_attempts(data_id)
                        except Exception as e:
                            st.error(f"Error decrypting data: {str(e)}")
                    else:
                        attempts = st.session_state.storage_manager.increment_failed_attempts(data_id)
                        st.error(f"❌ Incorrect passkey! Attempts remaining: {3 - attempts}")
                        
                        if attempts >= 3:
                            st.warning("🔒 Too many failed attempts! Please authenticate to continue.")
                            st.session_state.authenticated = False
                            st.session_state.current_data_id = data_id
                            st.session_state.page = "login"
                            st.experimental_rerun()

# Initialize page in session state if not exists
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Navigation sidebar
st.sidebar.title("Navigation")
if st.sidebar.button("🏠 Home"):
    st.session_state.page = "home"
if st.sidebar.button("📝 Store Data"):
    st.session_state.page = "store"
if st.sidebar.button("🔍 Retrieve Data"):
    st.session_state.page = "retrieve"

# Main app logic
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "home":
    home_page()
elif st.session_state.page == "store":
    store_data_page()
elif st.session_state.page == "retrieve":
    retrieve_data_page()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("🔒 Secure Data Encryption System\n\nVersion 1.0") 